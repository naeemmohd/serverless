'use strict';

var AWS = require("aws-sdk");
AWS.config.update({region: "us-east-1"});
var db = new AWS.DynamoDB.DocumentClient();

module.exports.get = (event, context, callback) => {
    
    const data = event.queryStringParameters;
    const params = {
        TableName: "PaymentBalance",
        Key: {
          InvoiceID: parseInt(data.InvoiceID)
        }
    };
    
    db.get(params, (err, result) => {
        if (err) {
            console.error(err);
            const errorResponse = {
                statusCode: err.statusCode || 501,
                headers: { 'Content-Type': 'text/plain'},
                body: JSON.stringify('Sorry, Cound not get the item for:' + data.InvoiceID),
            };
            callback(null, errorResponse);
            return;
        };

        const successResponse = {
            statusCode: 200,
            body: "Retrieved Item successfully. " + JSON.stringify(result),
        };
        callback(null, successResponse);
    });
};

