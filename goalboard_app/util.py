from datetime import timedelta, datetime, timezone

class GoalboardSpreadsheet:
    def __init__(self, user):
        self.user = user
        self.worksheets = self._get_worksheets()

    def _get_worksheets(self):
        if datetime.now(timezone.utc) - self.user.updated > timedelta(minutes=1) or not self.user.spreadsheet_data:
            self.spreadsheet = self.user.gc.open_by_key(self.user.spreadsheetId)
            self._system = self.spreadsheet.worksheet('system').range('A1:C4')
            self.row_counts = [self._system[i:i + 3] for i in range(0, len(self._system), 3)]
            self.worksheets = {row[0].value: [x.value for x in self.spreadsheet.worksheet(row[0].value).range(f'A{int(row[2].value)+1}:E{row[1].value}')] for row in self.row_counts}
            self.worksheets = {x: [y[i:i+5] for i in range(0, len(y), 5)] for x, y in self.worksheets.items()}
            self._update_user()
        else:
            self.worksheets = self.user.spreadsheet_data
        return self.worksheets

    def _update_user(self):
        if hasattr(self, 'worksheets') and isinstance(self.worksheets, dict):
            self.user.spreadsheet_data = self.worksheets
            self.user.save()

    @property
    def whoami(self):
        worksheet = self.worksheets['whoami']
        return [x[0] for x in worksheet]

    @property
    def goals(self):
        worksheet = self.worksheets['goals']
        goals_list = []
        for goal in worksheet:
            goal_name = goal[0]
            goal_values = list(map(
                lambda x: x == 'TRUE' if x in ('FALSE', 'TRUE') else int(x) if x.isdigit() else x,
                goal[1:]
            ))
            checks = [
                bool((goal_values[0] or goal_values[1]) and goal_values[2]),
                all(goal_values),
                any(map(lambda x: not isinstance(x, int) and x.isalpha(), goal_values)),
                (goal_values[2] != '' and not isinstance(goal_values[2], bool)),
                not isinstance(goal_values[1], int) and not isinstance(goal_values[2], bool),
                (goal_values[0] == '' and not isinstance(goal_values[1], int)) and not isinstance(goal_values[2], bool)
            ]
            if any(checks):
                continue
            goal_dict = {
                'name': goal_name,
                'type': 'binary' if isinstance(goal_values[2], bool) else 'measurable',
                'done': goal_values[0],
                'planned': goal_values[1],
                'status': goal_values[2],
                'percentage': int((goal_values[2] if isinstance(goal_values[2], bool) else goal_values[0]/goal_values[1])*100)
            }
            goals_list.append(goal_dict)
        return goals_list
