import csv


class kseCsvHandler():
    def __init__(self, path):
        self.path = path
        self.opening = []
        self.hold = []
        self.closing = []

    def load_csv(self):
        """
        read all valve csv data
        :return:
        """
        with open(self.path) as csv_file:
            parameters = csv.reader(csv_file, delimiter=';')

            for ndx, row in enumerate(parameters):  # all rows
                # print(', '.join(row))
                if ndx > 3:  # if not header
                    for row_ndx, cell in enumerate(row):  # all columns
                        if row_ndx == 1 and cell:  # opening ramp
                            self.opening.append(cell)
                        elif row_ndx == 3 and cell:  # hold ramp
                            self.hold.append(cell)
                        elif row_ndx == 7 and cell:  # closing ramp
                            self.closing.append(cell)


