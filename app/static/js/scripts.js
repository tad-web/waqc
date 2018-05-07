$(document).on("click", ".toggleExtraNoticesBtn", function(e) {
  const id = e.target.id
  $(`.extra-${id}`).toggleClass('hidden');
});


/*
 * Selects all of the text of all of the children within the element at the specified id, copies
 *   that text to the clipboard, and then unselects all the text
 * @param {string} id - the id of the element to copy to the clipboard
 */
function copyToClipboard(id) {
  window.getSelection().selectAllChildren(document.getElementById(id));
  document.execCommand("Copy");
  window.getSelection().removeAllRanges();
}
