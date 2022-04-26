function deleteArticle(borrowed_id, book_title) {
    var message = "Are you sure to delete this data " + book_title + " ?";
    var confirm_delete = confirm(message);

    // value of confirm() function is True if user clicks on OK
    if (confirm_delete == true) {
        // use axios to call delete, with the article id to delete
        var url = "/delete" + borrowed_id;
        axios({
            method: "POST",
            url: url,
        }).then(
            (response) => {
                var data = response.data;
                if (data.redirect) {
                    window.location.href = data.redirect;
                }
            }
        );
    }
}
