// Please enter the actual APIGATEWAYURL from the API Gateway Screen
var APIGATEWAYURL = 'https://p0gtmoln90.execute-api.us-east-1.amazonaws.com/prod';

// setup divs for error, success and results
var divError = document.getElementById('error-msg')
var successDiv = document.getElementById('success-msg')
var resultsDiv = document.getElementById('results-msg')

var invoiceID = document.getElementById('InvoiceID')
var billingAmount = document.getElementById('BillingAmount')
var billersName = document.getElementById('BillersName')
var cardNumber = document.getElementById('CardNumber')
var expiryDate = document.getElementById('ExpiryDate')
var emailId = document.getElementById('EmailId')
var phnNumber = document.getElementById('PhnNumber')

var postPaymentButton = document.getElementById('postPaymentButton')

// setup functions to get the field data
function getInvoiceID() { return invoiceID.value }
function getBillingAmount() { return billingAmount.value }
function getBillersName() { return billersName.value }
function getCardNumber() { return cardNumber.value }
function getExpiryDate() { return expiryDate.value }
function getEmailId() { return emailId.value }
function getPhnNumber() { return phnNumber.value }

function clearMessageDivs(state) {
    // clear the error, sucess and results div to refresh the content
    divError.textContent = '';
    resultsDiv.textContent = '';
    successDiv.textContent = '';
    
    invoiceID.disabled = false;
    billersName.disabled = true;
    billingAmount.disabled = true;
    
    if(state == 'get'){
        cardNumber.disabled = false;
        expiryDate.disabled = false;
        emailId.disabled = false;
        phnNumber.disabled = false;
        postPaymentButton.disabled = false;
    }
    else{
        cardNumber.disabled = true;
        expiryDate.disabled = true;
        emailId.disabled = true;
        phnNumber.disabled = true;
        postPaymentButton.disabled = true;
    }
    
    

    
}

clearMessageDivs('load');

// Add the click listeners for both buttons button that make the API request

document.getElementById('getBalanceButton').addEventListener('click', function (event) {
    // prevent page reloading by  clear message Divs
    event.preventDefault()
    clearMessageDivs('get')
    // Call the GET API service by Passing the InvoiceID
    fetch(APIGATEWAYURL+ '/paymentbalance/id?InvoiceID='+getInvoiceID(), {
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
        invoiceID.value = data.Item.InvoiceID;
        billersName.value = data.Item.CustomerName;
        billingAmount.value = data.Item.Balance;
    })
    .catch(function(err) {
        divError.textContent = 'Sorry, We could not pull your bill details:\n' + err.toString();
        console.log(err)
    });
});

document.getElementById('postPaymentButton').addEventListener('click', function (event) {
    // prevent page reloading by  clear message Divs
    event.preventDefault()
    clearMessageDivs('post')    
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

