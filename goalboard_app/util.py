from time import time

class GoalboardSpreadsheet:
    def __init__(self, user):
        start = time()
        self.spreadsheet = user.gc.open_by_key(user.spreadsheetId)
        self._system = self.spreadsheet.worksheet('system').range('A1:B4')
        self.row_counts = [self._system[i:i + 2] for i in range(0, len(self._system), 2)]
        self.worksheets = {row[0].value: list(map(lambda x: x.value, self.spreadsheet.worksheet(row[0].value).range(f'A1:E{row[1].value}'))) for row in self.row_counts}
        print('init', time() - start, self.worksheets)

    @property
    def whoami(self):
        worksheet = self.worksheets['goals']
        return worksheet[1:]

    @property
    def goals(self):
        start = time()
        worksheet = [self.worksheets['goals'][i:i + 4] for i in range(0, len(self.worksheets['goals']), 4)]
        goals_list = []
        for goal in worksheet[1:]:
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
            goals_list.append({
                'name': goal_name,
                'type': 'binary' if isinstance(goal_values[2], bool) else 'measurable',
                'done': goal_values[0],
                'planned': goal_values[1],
                'status': goal_values[2]
            })
        return goals_list
