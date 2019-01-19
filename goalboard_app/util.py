from time import time

class GoalboardSpreadsheet:
    def __init__(self, user):
        start = time()
        self.spreadsheet = user.gc.open_by_key(user.spreadsheetId)
        self._system = self.spreadsheet.worksheet('system').range('A1:C4')
        self.row_counts = [self._system[i:i + 3] for i in range(0, len(self._system), 3)]
        self.worksheets = {row[0].value: [x.value for x in self.spreadsheet.worksheet(row[0].value).range(f'A{int(row[2].value)+1}:E{row[1].value}')] for row in self.row_counts}
        self.worksheets = {x: [y[i:i+5] for i in range(0, len(y), 5)] for x, y in self.worksheets.items()}

    @property
    def whoami(self):
        worksheet = self.worksheets['whoami']
        return [x[0] for x in worksheet]

    @property
    def goals(self):
        start = time()
        worksheet = self.worksheets['goals']
        print(worksheet)
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
            print(goal_name, checks)
            if any(checks):
                continue
            goals_list.append({
                'name': goal_name,
                'type': 'binary' if isinstance(goal_values[2], bool) else 'measurable',
                'done': goal_values[0],
                'planned': goal_values[1],
                'status': goal_values[2]
            })
        print(goals_list)
        return goals_list
