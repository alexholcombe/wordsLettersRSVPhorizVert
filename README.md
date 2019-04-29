    myDlg.addField('firstCondition (0 = Letters, 1 = Words):', firstCondition, tip=str(firstCondition))

            if condition==1:
                wordBin = thisTrial['bin']
            else:
                wordBin = SampleLetters

VERTICAL NOT EQUIDISTANT

configuration =  'vertical' #'horizontal' 
Why aren't cues drawing in situation of precueFrames

Only the first trial seems to be having timing errors.

## MBL

- Need to add SOA field to data frame and exclude longer practice SOAs from mixture modeling
- Should probably run him on a few dozen more trials in the hopes of bringing the SOA=-1 and SOA=+1 number of errors above chance.