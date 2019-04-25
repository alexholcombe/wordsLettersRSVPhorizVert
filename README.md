    myDlg.addField('firstCondition (0 = Letters, 1 = Words):', firstCondition, tip=str(firstCondition))

            if condition==1:
                wordBin = thisTrial['bin']
            else:
                wordBin = SampleLetters