const processBtn = document.getElementById('process-btn');
const searchBtn = document.getElementById('search-button');
const modalSubmitBtn = document.getElementById('modal-submit-btn');

const checkboxes = document.querySelectorAll('input[type="checkbox"]');
const searchInput = document.getElementById('search-input');
const filterOptions = document.getElementById('filter-options');
const transactionType = document.querySelectorAll('select[name="transaction_type"]');

const nextPageLink = document.getElementById('next');
const lastPageLink = document.getElementById('last');
const previousPageLink = document.getElementById('previous');
const firstPageLink = document.getElementById('first');
const currentPage = document.getElementById('current');

let selectedVendorsInvoiceNumber = [];
let selectedPageNumber = 1;
let numberOfPages = 0;
let hasClickedOnSearchBtn = false;
let query_params = [];
let selectedTransactionType = {};

sessionStorage.clear();
// Retrieve the checkbox and select values from sessionStorage
//updateTransactionType();
addCheckBoxandSelectValues(transactionType, checkboxes);
addEventListenerToCheckboxes(checkboxes);
addEventListenerToSelect(transactionType);
addEventListenerToAnchorTag();

function addEventListenerToCheckboxes(checkboxes) {
    /**
     * Add event listener to checkboxes
     * if checked the checkbox value added to sessionStorage and VendorInvoiceNumber array, process button disabled
     * when unchecked checkbox value removed from sessionStorage and VendorInvoiceNumber array
     */
    checkboxes.forEach(cb => {
        cb.addEventListener('change', () => {
            if (cb.checked) {
                const value = cb.value;
                const checked = cb.checked
                addSelectedVendorsInvoiceNumber(cb.value);
                sessionStorage.setItem(value, checked);
                saveSelectedRows('table-body');
            } else {
                const value = cb.value;
                selectedVendorsInvoiceNumber = selectedVendorsInvoiceNumber.filter(vendor => vendor !== value);
                sessionStorage.removeItem(value);
            }
            const isChecked = Array.from(checkboxes).some(cb => cb.checked);
            processBtn.disabled = !isChecked;
        });
    });
}


/*function addEventListenerToSelect(transactionType) {
    transactionType.forEach(transaction => {
        transaction.addEventListener('change', () => {
            document.querySelectorAll('input[name="transaction"]').forEach(
                cb=>{
                    cb.removeAttribute('disabled');
                }
            )
            const value = transaction.value;
            const rowId = transaction.closest('tr').id;
            if (value) {
                sessionStorage.setItem(rowId, value);
            } else {
                sessionStorage.removeItem(rowId);
            }
            saveSelectedRows('table-body');
        });
    });

}*/
function addEventListenerToSelect(transactionType) {
  transactionType.forEach(transaction => {
    transaction.addEventListener('change', () => {
      const value = transaction.value;
      const row = transaction.closest('tr');
      const inputElement = row.querySelector('input[name="transaction"]');

      if (value) {
        inputElement.removeAttribute('disabled');
      } else {
        inputElement.setAttribute('disabled', 'disabled');
      }

      const rowId = row.id;
      if (value) {
        sessionStorage.setItem(rowId, value);
      } else {
        sessionStorage.removeItem(rowId);
      }

      saveSelectedRows('table-body');
    });
  });
}

 function updateTransactionType() {
    const table = document.querySelector("#table-body")
        const rows = table.querySelectorAll('tr');
        rows.forEach(row => {
            const accountNumber = row.querySelector('#acc_no').textContent;
            fetch(`account_number/?acc_no=${accountNumber}`)
                .then(data => data.json())
                .then(d => {
                    if (d.resp.length === 0) {
                        const transaction_type = row.querySelectorAll('select[name="transaction_type"]');
                        transaction_type.forEach(t => {
                            const option = t.querySelectorAll('option')
                            option.forEach(opt => {
                                if (opt.value === 'IFT') {
                                    opt.classList.add('d-none')
                                }
                            })
                        });
                    }
                });
        });
    }
function addSelectedVendorsInvoiceNumber(invoiceId) {
    /**
     * Add selected vendors to array
     */
    if (!selectedVendorsInvoiceNumber.includes(invoiceId)) {
        selectedVendorsInvoiceNumber.push(invoiceId);
        console.log(selectedVendorsInvoiceNumber);
    }
}

function saveSelectedRows(tableID) {
    let rows = document.querySelectorAll(`#${tableID} tr`);
    rows.forEach((row) => {
            let cb = row.querySelector('td input[type="checkbox"]')
            if (cb.checked) {
                let transactionType = row.querySelector('td select[name="transaction_type"]').value;

                selectedTransactionType[cb.value] = transactionType;
            }
        }
    )
}

function createTableBody(transactionInfo, vendorInfo, tableBodyID) {
    /**
     * Create new table body elements and add them to the table body
     * @param {Array} transactionInfo - Array of transaction objects
     * @param {Array} vendorInfo - Array of vendor objects
     * @param {String} tableBodyID - ID of table body element
     */

    let tableBody = document.getElementById(tableBodyID);
    tableBody.innerHTML = '';

    // Add new transactions
    if (transactionInfo.length > 0) {
        for (transaction of transactionInfo) {

            transaction = JSON.parse(transaction);
            const tr = document.createElement('tr');
            tr.setAttribute("id", "select-" + transaction.IDINVC);
            tr.innerHTML = `
             <td>
                 <input type="checkbox" name="transaction" id="transaction-checkbox" value="${transaction.IDINVC}">
            </td>
            <td>${transaction.DATERMIT}</td>
            <td>${transaction.AMTPAYM}</td>
            <td>${transaction.IDINVC}</td>
            <td>${transaction.IDVEND}</td>
      `;
            for (vendor of vendorInfo) {
                if (transaction.IDVEND === vendor.vendor_id) {
                    tr.innerHTML += `
            <td>${vendor.account_name}</td>
            <td id="acc_no">${vendor.account_no}</td>
            <td>${vendor.sort_code}</td>
          `;
                }
            }
            tr.innerHTML += `
                <td>
            <select class="form-select form-select-sm" name="transaction_type">
            <option>---</option>
            <option value="IFT" >INTERNAL FUNDS TRANSFER</option>
            <option value="DDAC">DDAC</option>
            <option value="RTGS">RTGS</option>
            </select>
        </td>`


            tableBody.appendChild(tr);
        }

    } else {
        const tr = document.createElement('tr');
        tr.innerHTML = `
      <td colspan="8" class="text-center">No transactions found</td>
    `;
        tableBody.appendChild(tr);
    }


}

function addCheckBoxandSelectValues(transactionType, checkboxes) {
    checkboxes.forEach(checkbox => {
        const value = checkbox.value;
        const checked = JSON.parse(sessionStorage.getItem(value));

        // If the checkbox was checked before, set it to checked
        if (checked) {
            checkbox.checked = true;
        }
    });
    transactionType.forEach(transaction => {
        const rowId = transaction.closest('tr').id;
        const selectValue = sessionStorage.getItem(rowId);
        // Set the select tag to the previous value if it exists
        if (selectValue) {
            transaction.value = selectValue;
        }
    })

}

function addEventListenersAndPopulateFields() {
    /**
     *  Get all checkboxes, add event listener to them and check if they are checked or not
     */
    let checkboxes = document.querySelectorAll('input[type="checkbox"]');
    let transactionType = document.querySelectorAll('select[name="transaction_type"]');

    addEventListenerToSelect(transactionType);
    addEventListenerToCheckboxes(checkboxes);
    addCheckBoxandSelectValues(transactionType, checkboxes);
    console.log(sessionStorage)
}

// handles the click even of the anchor tags
function handleClick(event) {
    event.preventDefault();
    const url = event.target.getAttribute('href');
    fetch(url)
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const newDoc = parser.parseFromString(html, 'text/html');
            const newSelect = newDoc.querySelectorAll("select[name='transaction_type']");
            const newCheckboxes = newDoc.querySelectorAll('input[type="checkbox"]');
            addCheckBoxandSelectValues(newSelect, newCheckboxes);
            addEventListenerToSelect(newSelect);
            addEventListenerToCheckboxes(newCheckboxes)
            const newTable = newDoc.getElementById('table-body')
            const newPaginator = newDoc.getElementById('paginator');
            document.getElementById('table-body').replaceWith(newTable);
            document.getElementById('paginator').replaceWith(newPaginator);
            updateTransactionType();
            addEventListenerToAnchorTag();
        });
}

function addEventListenerToAnchorTag() {
    const paginationLinks = document.querySelectorAll('.custom-pagination a');
    paginationLinks.forEach(link => {
        link.addEventListener('click', handleClick); // Add the handleClick function as the event listener
    });
}

function removeEventListenerFromAnchorTag() {
    const paginationLinks = document.querySelectorAll('.custom-pagination a');
    paginationLinks.forEach(link => {
        link.removeEventListener('click', handleClick); // Remove the handleClick function as the event listener
    });
}

async function searchDatabase(searchParams, filterOptions) {
    /**
     * Send request to database to search for vendor transactions
     * and vendor information that matches the search parameters
     * @param {String} searchParams - String containing search parameters
     * @param {String} filterOptions - String containing filter options
     * @return {Array} - Object containing transaction info and vendor info
     * */

        // Send ajax request to server to retrieve matching vendors
    const res = await fetch(`search/?search_params=${searchParams}&filter_options=${filterOptions}&page_number=1`);

    return await res.json();
}

searchBtn.addEventListener('click', (e) => {
    e.preventDefault();
    hasClickedOnSearchBtn = true;

    // Query the database for the specified search parameters
    let queryResults = searchDatabase(searchInput.value, filterOptions.value);

    // Display the results in the table body
    queryResults.then((data) => {
        createTableBody(data.transaction_info, data.vendor_info, 'table-body');
        removeEventListenerFromAnchorTag();
        addEventListenersAndPopulateFields()
        numberOfPages = data.number_of_pages;
        currentPage.textContent = `Showing 1 of ${numberOfPages} Pages.`;
        query_params = [searchInput.value, filterOptions.value]
        checkIfFirstPage();
        checkIfLastPage();
        checkIfPageHasNextOrPreviousPage();
        updateTransactionType();


    }).catch((err) => {
        console.log(err)
    });
});

modalSubmitBtn.addEventListener('click', (e) => {
    e.preventDefault()
    // Send selected invoice numbers & transaction type to server using ajax
    $.ajax({
        type: 'POST',
        url: 'post-transactions/',
        data: {
            'csrfmiddlewaretoken': getCSRFToken(),
            'invoice_ids[]': JSON.stringify(selectedVendorsInvoiceNumber),
            'transaction_type': JSON.stringify(selectedTransactionType),
        },
        dataType: 'json',
    }).then(res => {
        console.log(res.stats)
        if (res.stats !== 200) {
            Swal.fire({
                icon: 'error',
                title: 'Your Request Could Not Be processed:',
                text: res.resps,
                confirmButtonText: "OK",
                timer: 2000,
                footer: 'Try Again Later'
            })
            $('#post-transaction-modal').modal('hide');
        } else {
            Swal.fire({
                icon: 'success',
                title: 'Your Request Has Been Successfully Processed:',
                confirmButtonText: "OK",
                timer: 2000,
                text: res.resps,
            }).then(() => {
                window.location.href = 'dashboard';
            });
        }

    }).catch(err => console.log(err));

});

processBtn.addEventListener('click', (e) => {
    console.log("clicked");
    e.preventDefault();

    $.ajax({
        type: 'POST',
        url: 'search-invoices/',
        data: {
            'csrfmiddlewaretoken': getCSRFToken(),
            'invoice_ids[]': JSON.stringify(selectedVendorsInvoiceNumber),
        },
        dataType: 'json',
    }).then(transactions => {
        console.log(transactions)
        createTableBody(transactions.transaction_info, transactions.vendor_info, 'modal-table-body');
        addEventListenersAndPopulateFields();
    }).catch(err => console.log(err));

});

// Add event listener to change page links


function getCSRFToken() {
    let csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
    if (csrfToken == null) {
        csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    }
    return csrfToken;
}

function checkIfPageHasNextOrPreviousPage() {
    if (selectedPageNumber === 1) {
        previousPageLink.classList.add('d-none');
        if (numberOfPages === 1) {
            nextPageLink.classList.add('d-none');
            firstPageLink.classList.add('d-none');
            lastPageLink.classList.add('d-none');
            previousPageLink.classList.add('d-none');
        }
    } else {
        previousPageLink.classList.remove('d-none');
    }

    if (selectedPageNumber === numberOfPages) {
        nextPageLink.classList.add('d-none');
    } else {
        nextPageLink.classList.remove('d-none');
    }
}

function nextPage() {
    /**
     *  Go to next page
     */
    if (selectedPageNumber !== numberOfPages) {
        selectedPageNumber += 1;
    }

    goToPage(`search/`, 'table-body');

}

function previousPage() {
    /**
     *  Go to previous page
     */
    if (selectedPageNumber !== 1) {
        selectedPageNumber -= 1;
    }

    goToPage(`search/`, 'table-body');
}

function checkIfLastPage() {
    /**
     * Check If the selected page is the last page
     * */

    if (selectedPageNumber === numberOfPages) {
        lastPageLink.classList.add('d-none');
    } else {
        lastPageLink.classList.remove('d-none');
    }

}

function checkIfFirstPage() {
    /**
     * Check if the selected page is the first page
     * */
    if (selectedPageNumber === 1) {
        firstPageLink.classList.add('d-none');
    } else {
        firstPageLink.classList.remove('d-none');
    }
}

async function goToPage(url, tbody) {
    /**
     *  Get New Paginated Page Data, Pagination Page Number and Number of Pages
     *  @param {String} url - URL to send ajax request to
     *  @param {String} tbody - ID of table body element
     */
    currentPage.textContent = `Showing ${selectedPageNumber} of ${numberOfPages} Pages`;

    checkIfFirstPage();
    checkIfLastPage();
    checkIfPageHasNextOrPreviousPage();

    try {
        // Send ajax request to server to retrieve new paginated data
        const res = await fetch(`${url}?search_params=${query_params[0]}&filter_options=${query_params[1]}&page_number=${selectedPageNumber}`);
        const data = await res.json();
        const transactionInfo = data.transaction_info;
        const vendorInfo = data.vendor_info;

        // Create new table body
        createTableBody(transactionInfo, vendorInfo, tbody, 'goToPage Function');
        // Get checkboxes
        addEventListenersAndPopulateFields();
    } catch (err) {
        console.log(err);
    }
}


nextPageLink.addEventListener('click', (e) => {
    if (hasClickedOnSearchBtn === true) {
        e.preventDefault();
        nextPage();
    }
});

previousPageLink.addEventListener('click', (e) => {
    if (hasClickedOnSearchBtn === true) {
        e.preventDefault();
        previousPage();
    }
});

lastPageLink.addEventListener('click', (e) => {
    if (hasClickedOnSearchBtn === true) {
        e.preventDefault();
        selectedPageNumber = numberOfPages;
        goToPage(`search/`, 'table-body');
    }
});

firstPageLink.addEventListener('click', (e) => {
    if (hasClickedOnSearchBtn === true) {
        e.preventDefault();
        selectedPageNumber = 1;
        goToPage(`search/`, 'table-body');
    }
});




