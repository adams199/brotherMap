/** @OnlyCurrentDoc */

function formatForNewGeo() {
  var spreadsheet = SpreadsheetApp.getActive();
  spreadsheet.getRange('A:C').activate()
  .trimWhitespace();
  spreadsheet.getActiveSheet().sort(1, false);
  spreadsheet.getActiveRange().offset(1, 0, spreadsheet.getActiveRange().getNumRows() - 1).activate();
  spreadsheet.getActiveRange().removeDuplicates([3]).activate();
};