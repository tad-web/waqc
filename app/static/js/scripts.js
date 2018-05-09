/*
 * Selects all of the text of all of the children within the element at the specified id, copies
 *   that text to the clipboard, and then unselects all the text
 * @param {string} id - the id of the element to copy to the clipboard
 */
function copyToClipboard(id) {
  window.getSelection().selectAllChildren(document.getElementById(id));
  document.execCommand('Copy');
  window.getSelection().removeAllRanges();
}


/*
 * Meant to be the onclick for toggleExtraNoticesBtn buttons. Toggles the hidden class on
 *   the appropriate extraNotices and changes the text of the button appropriately.
 * @param {event} e
 */
function toggleExtraNotices(e) {
  const btn = e.target
  $('.extra-' + btn.id).toggleClass('hidden');

  const url = $('h2')[btn.getAttribute('data-url-index')].textContent.split(' ')[1];
  const noticeType = $('h3')[btn.getAttribute('data-notice-type-index')].textContent.split('s:')[0];
  if($('.extra-' + btn.id).is(':hidden')) $('#' + btn.id).text('Show all ' + noticeType + ' violations for ' + url);
  else $('#' + btn.id).text('Hide all but three ' + noticeType + ' violations for ' + url);
}
