// Please enter the actual APIGATEWAYURL from the API Gateway Screen
var APIGATEWAYURL = 'https://example1a2s3d.execute-api.us-east-1.amazonaws.com/dev/prometheon';

// setup divs for error, success and results
var divError = document.getElementById('error-msg')
var successDiv = document.getElementById('success-msg')
var resultsDiv = document.getElementById('results-msg')


// setup functions to get the field data
function getInvoiceID() { return document.getElementById('InvoiceID').value }
function getBillersName() { return document.getElementById('BillersName').value }
function getCardNumber() { return document.getElementById('CardNumber').value }
function getExpiryDate() { return document.getElementById('ExpiryDate').value }
function getEmailId() { return document.getElementById('EmailId').value }
function getPhnNumber() { return document.getElementById('PhnNumber').value }

function clearMessageDivs() {
    // clear the error, sucess and results div to refresh the content
    divError.textContent = '';
    resultsDiv.textContent = '';
    successDiv.textContent = '';
}

// Add the click listeners for both buttons button that make the API request

document.getElementById('getBalanceButton').addEventListener('click', function (event) {
    // prevent page reloading by  clear message Divs
    event.preventDefault()
    clearMessageDivs()
    // Call the GET API service by Passing the InvoiceID
    fetch(APIGATEWAYURL+'/id?InvoiceID='+getInvoiceID(), {
        headers:{
            "Content-type": "application/json"
        },
        method: 'GET',
        mode: 'cors'
    })
    .then((resp) => resp.json()) 
    .then(function(data) {
        console.log(data)
        successDiv.textContent = 'Please check your balance and make proper payment.';
        resultsDiv.textContent = JSON.stringify(data);
    })
    .catch(function(err) {
        divError.textContent = 'Sorry, We could not pull your bill details:\n' + err.toString();
        console.log(err)
    });
});

document.getElementById('postPaymentButton').addEventListener('click', function (event) {
    // prevent page reloading by  clear message Divs
    event.preventDefault()
    clearMessageDivs()    
    // Prepare the appropriate HTTP request to the API with fetch
    // update uses the /prometheon/id endpoint and requires a JSON payload
    fetch(APIGATEWAYURL+'/id', {
        headers:{
            "Content-type": "application/json"
        },
        method: 'PUT',
        body: JSON.stringify({
            'InvoiceID': getInvoiceID(),
            'BillersName': getBillersName(),
            'CardNumber': getCardNumber(),
            'ExpiryDate': getExpiryDate(),
            'EmailId': getEmailId(),
            'PhnNumber': getPhnNumber()
        }),
        mode: 'cors'
    })
    .then((resp) => resp.json()) 
    .then(function(data) {
        console.log(data)
        successDiv.textContent = 'Congratulations, Your payment has been posted and an email/SMS has been sent you.';
        resultsDiv.textContent = JSON.stringify(data);

    })
    .catch(function(err) {
        divError.textContent = 'Sorry, we could not process your payment request:\n' + err.toString();
        console.log(err)
    });
});

