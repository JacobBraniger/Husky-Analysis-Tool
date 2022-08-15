# HuskyConfigTool
This is a project to analyze the machine data output of husky plastic injection machines. Developed by Jacob Braniger in the Greencastle, IN location of of the Phoenix packaging company. This application reads a xlsx file created from the event log transfer of the machine, and then creates a new xlsx file detailing the time range of the analysis, the total running time of the machine within the time period, what percent of the total analysis period that is, and a breakdown of the cycle interruptions.
# How to Download
There are two versions. One that includes a large directory with a config file to change settings, and one that is just an exe. If you want the standalone exe, just download HuskyAnalysisToolNoConfig.exe. If you want the directory and config, downlad the entire HuskyAnalysisTool folder.
# Using the Software
First, download the event log file from the Husky Machine.
Next, convert the file into an excel workbook (*.xlsx).
Delete any rows of data that have more columns of data than there are headers. To find these, click on the column to the right of the last header, go to the data tab, and hit filter. Then open the filter dropdown menu and uncheck (Blanks). Delete all remaining rows, if there are any. These are unnecessary for the anlysis and will make the file unreadable. Make sure not to mess with anything else, and don't forget to save.
Once the data is prepped, run the .exe file.
Use the buttons to search for your data (the excel workbook) and choose a place for the program to out the analysis. Type a name into the bottom text box, and the press analyze. When finished, the program will write a message saying it's done.
If you want to analyze more files, just select the next one with the top button, and type a new name into the box. Press analyze again to start the next analysis.
Close the program when you're done.
# Demo


https://user-images.githubusercontent.com/46425131/184659639-62cea4e0-8e08-4ced-b7de-1a60e364a034.mp4
