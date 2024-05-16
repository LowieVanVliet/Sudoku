import time
import csv
class Field:
        def __init__(self,RN,CN,BN,Value,Possibles):
            self.RN = RN
            self.CN = CN
            self.BN = BN
            self.Value = Value
            self.Possibles = Possibles
            
def display(fieldlist):
    for i in range(9):
        if i % 3 == 0:
            print("+" + "-" * 23 + "+")
        for j in range(9):
            if j % 3 == 0:
                print("|", end=" ")
            field = fieldlist[i * 9 + j]
            print(field.Value if field.Value != 0 else '-', end=" ")
            if j == 8:
                print("|")
    print("+" + "-" * 23 + "+")

    
def newfields(puzzlearray):
        Puzzle = list(puzzlearray)
        fieldlist = []
        i = 0
        while i < 81:
                RN = i//9 + 1
                CN = i%9 + 1
                BN = ((CN-1)//3+1)+ 3*((RN-1)//3)
                Value = int(Puzzle[i])
                if Value == 0:
                        Possibles = set('123456789')
                else: Possibles = set(str(Value))
                fieldlist.append(Field(RN,CN,BN,Value,Possibles))
                i += 1
                # display(fieldlist)
        return fieldlist

def CheckSolved(unsolvedFields):
        for Field in unsolvedFields:
                count = 0
                for x in Field.Possibles:
                        count += 1
                if count == 1:
                        Field.Value = int(next(iter(Field.Possibles)))
                        unsolvedFields.remove(Field)
                        CheckSeenCells(Field,unsolvedFields)
                        
def CheckSeenCells(Field1,unsolvedCells):
        SeenCells = [Field for Field in unsolvedCells if (Field.RN == Field1.RN or Field.CN == Field1.CN or Field.BN == Field1.BN) and Field1.Possibles < Field.Possibles]
        for Field in SeenCells:
                Field.Possibles -= Field1.Possibles
                CheckSolved(unsolvedCells)
        
def CheckUnits(unsolvedFields):
        HasChanges = False
        for i in range(1,10):
                RowList = [Field for Field in unsolvedFields if Field.RN == i]
                ColumnList = [Field for Field in unsolvedFields if Field.CN == i]
                BoxList = [Field for Field in unsolvedFields if Field.BN == i]
                for j in range(1,10):
                        ListToCheck = [Field for Field in RowList if str(j) in Field.Possibles]
                        count = 0
                        for Field in ListToCheck:
                                count += 1
                        if count == 1:
                                for Field in ListToCheck:
                                        Field.Value = j
                                        Field.Possibles = set(str(j))
                                        CheckSeenCells(Field,unsolvedFields)
                                      #  print('Filled in ' + str(j) + ' in field ' + str((Field.RN,Field.CN)))
                                HasChanges = True
                
                        ListToCheck = [Field for Field in ColumnList if str(j) in Field.Possibles]
                        count = 0
                        for Field in ListToCheck:
                                count += 1
                        if count == 1:
                                for Field in ListToCheck:
                                        Field.Value = j
                                        Field.Possibles = set(str(j))
                                        CheckSeenCells(Field,unsolvedFields)
                                       # print('Filled in ' + str(j) + ' in field ' + str((Field.RN,Field.CN)))
                                HasChanges = True
                        ListToCheck = [Field for Field in BoxList if str(j) in Field.Possibles]
                        count = 0
                        for Field in ListToCheck:
                                count += 1
                        if count == 1:
                                for Field in ListToCheck:
                                        Field.Value = j
                                        Field.Possibles = set(str(j))
                                        CheckSeenCells(Field,unsolvedFields)
                                        # print('Filled in ' + str(j) + ' in field ' + str((Field.RN,Field.CN)))
                                        HasChanges = True
        return HasChanges

def CheckHiddenTuples(unsolvedFields,n):
        HasChanges = False
        ListOfTuples = [Field for Field in unsolvedFields if len(Field.Possibles) == n]
        for Field_Check in ListOfTuples:
                ListOfTuples.remove(Field_Check)
                SamePossibles = [Field for Field in ListOfTuples if Field.Possibles == Field_Check.Possibles]
                for FieldToCheck in SamePossibles:
                        if FieldToCheck.RN == Field_Check.RN:
                                SameRow = [Field for Field in unsolvedFields if Field_Check.Possibles < Field.Possibles and Field.RN == Field_Check.RN]
                                for Field1 in SameRow:
                                        #print(str(Field1.Possibles),Field1.RN, Field1.CN, Field_Check.Possibles, Field_Check.RN,Field_Check.CN,FieldToCheck.RN,FieldToCheck.CN)
                                        Field1.Possibles -= Field_Check.Possibles
                                        HasChanges = True
                                       # print(str(Field1.Possibles),Field1.RN, Field1.CN, Field_Check.Possibles, Field_Check.RN,Field_Check.CN,FieldToCheck.RN,FieldToCheck.CN)
                        if FieldToCheck.CN == Field_Check.CN:
                                SameColumn = [Field for Field in unsolvedFields if Field_Check.Possibles < Field.Possibles and Field.CN == Field_Check.CN]
                                for Field1 in SameColumn:
                                       # print(str(Field1.Possibles),Field1.RN, Field1.CN, Field_Check.Possibles, Field_Check.RN,Field_Check.CN,FieldToCheck.RN,FieldToCheck.CN)
                                        Field1.Possibles -= Field_Check.Possibles
                                        HasChanges = True
                                        #print(str(Field1.Possibles),Field1.RN, Field1.CN, Field_Check.Possibles, Field_Check.RN,Field_Check.CN,FieldToCheck.RN,FieldToCheck.CN)
                        if FieldToCheck.BN == Field_Check.BN:
                                SameBox = [Field for Field in unsolvedFields if Field_Check.Possibles < Field.Possibles and Field.BN == Field_Check.BN]
                                for Field1 in SameBox:
                                       # print(str(Field1.Possibles),Field1.RN, Field1.CN, Field_Check.Possibles, Field_Check.RN,Field_Check.CN,FieldToCheck.RN,FieldToCheck.CN)
                                        Field1.Possibles -= Field_Check.Possibles
                                        HasChanges = True
                                       # print(str(Field1.Possibles),Field1.RN, Field1.CN, Field_Check.Possibles, Field_Check.RN,Field_Check.CN,FieldToCheck.RN,FieldToCheck.CN)
                
        if HasChanges == True:
                CheckSolved(unsolvedFields)
        return HasChanges

def solveiteration(fieldlist):
        unsolvedFields = [Field for Field in fieldlist if Field.Value == 0]
        HasChanges = False
        FieldsToCheck = [Field for Field in fieldlist if Field.Value != 0]
        for fieldToCheck in FieldsToCheck:
                SeenFields = [Field for Field in unsolvedFields if str(fieldToCheck.Value) in Field.Possibles and(Field.RN == fieldToCheck.RN or Field.CN == fieldToCheck.CN or Field.BN == fieldToCheck.BN)]
                for Field in SeenFields:
                        Field.Possibles.remove(str(fieldToCheck.Value))
                        # print('Removed ' + str(i) + ' from possibles of field ' + str((Field.RN,Field.CN)))
                        HasChanges = True

        if HasChanges == True:
                CheckSolved(unsolvedFields)
        if CheckUnits(unsolvedFields) == True and unsolvedFields != []:
                HasChanges = True
                CheckSolved(unsolvedFields)
                #display(fieldlist)
        if CheckHiddenTuples(unsolvedFields,2) == True and unsolvedFields != []:
                HasChanges = True
        if HasChanges == True and unsolvedFields != []:
                solveiteration(fieldlist)
        else:
                return True
        
def solve(fieldlist):
       # display(fieldlist)   #uncomment this if you want the puzzle displayed
        
        Solved = False
        while Solved == False:
                Solved = solveiteration(fieldlist)
                
                #display(fieldlist)              #uncomment this if you want the solution displayed
        return [Field.Value for Field in fieldlist]
    
def solvebatch(batch):
        for line in batch:
                solve(newfields(line))
        
        
def Try(n,batchsize):
        with open('C:\\Users\\LowievanVliet\\Downloads\\sudoku.csv', 'r') as file:
        # Create a CSV reader object
                csv_reader = csv.reader(file)
                next(csv_reader)
                start_time = time.perf_counter()
                for _ in range(n):
                        batch = [next(csv_reader)[0] for _ in range(batchsize)]
                        solvebatch(batch)   
                end_time = time.perf_counter()
                duration = end_time - start_time
                print(duration)

def TryNoBatch(n):
        with open('C:\\Users\\LowievanVliet\\Downloads\\sudoku.csv', 'r') as file:
        # Create a CSV reader object
                csv_reader = csv.reader(file)
                next(csv_reader)
                start_time = time.perf_counter()
                batch = [next(csv_reader)[0] for _ in range(n)]
                solvebatch(batch)   
                end_time = time.perf_counter()
                duration = end_time - start_time
                print(duration)

    
while True:
        n = int(input("Enter the number of batches to iterate over: "))
        batchsize = int(input("Enter how large the batches should be: "))
        if n * batchsize == 0:

                break
        
        Try(n,batchsize)
    
    
