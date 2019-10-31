from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
import requests
import json

identity = 'Group16'
token = '411e25a9-5fff-42b5-8a2d-272f94b4a26f'
headers = {'identity': identity, 'token':token}

def index(request):
    return HttpResponse('OK')

def login_auth(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))

        username = request.POST.get('username')
        if user is not None:
            # GET customer id 
            response = requests.get("http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/customers/"+username, headers=headers)
            json_response = json.loads(response.text)
            customer_id = json_response['customerId']

            # GET customer details using customer id
            response = requests.get("http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/customers/"+ customer_id +"/details", headers=headers)
            json_response_customer = json.loads(response.text)
            first_name = json_response_customer['firstName']
            last_name = json_response_customer['lastName']

            # GET account details using customer id
            response = requests.get("http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/accounts/deposit/" + customer_id, headers=headers)
            json_response_account = json.loads(response.text)
            print(json_response_account)

            # TODO : handle case for multiple accounts. Currently handled for only one account
            account_id = json_response_account[0]['accountId']
            account_type = json_response_account[0]['type']
            account_display_name = json_response_account[0]['displayName']
            account_num = json_response_account[0]['accountNumber']

            # GET Transaction details using account_num, get only latest 10 transactions
            response = requests.get("http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/transactions/"+ str(account_id) +"?from=01-01-2018&to=01-31-2019", headers=headers)
            json_trans = json.loads(response.text)
            json_trans = json_trans[-10:] # get last 10 transactions

            tran_refs = []
            tran_types = []
            tran_amounts = []
            tran_dates = []
            
            for tran in json_trans:
                tran_refs.append(tran['referenceNumber'])
                tran_types.append(tran['type'])
                tran_amounts.append(tran['amount'])
                tran_dates.append(tran['date'][:10])

            zipped_list = zip(tran_refs, tran_types, tran_amounts, tran_dates)            

            return render(request, 'expense_app_polls/viewProfile.html' , {'account_id':account_id, 'firstname': first_name,'username':username,'zipped_list':zipped_list})
        else:
            return HttpResponse('Wrong Password')
    return HttpResponse('OK')

def login(request):
    return render(request, "expense_app_polls/base.html")


    user = authenticate(username='marytan', password='marypassword')
    if user is not None:
        # user is authenticated
        
        # GET customer id 
        response = requests.get("http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/customers/marytan", headers=headers)
        json_response = json.loads(response.text)
        customer_id = json_response['customerId']

        # GET customer details using customer id
        response = requests.get("http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/customers/"+ customer_id +"/details", headers=headers)
        json_response_customer = json.loads(response.text)
        first_name = json_response_customer['firstName']
        last_name = json_response_customer['lastName']

        # GET account details using customer id
        response = requests.get("http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/accounts/deposit/" + customer_id, headers=headers)
        json_response_account = json.loads(response.text)
        print(json_response_account)

        # TODO : handle case for multiple accounts. Currently handled for only one account
        account_id = json_response_account[0]['accountId']
        account_type = json_response_account[0]['type']
        account_display_name = json_response_account[0]['displayName']
        account_num = json_response_account[0]['accountNumber']

        # GET Transaction details using account_num, get only latest 10 transactions
        response = requests.get("http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/transactions/"+ str(account_id) +"?from=01-01-2018&to=01-31-2019", headers=headers)
        json_trans = json.loads(response.text)
        json_trans = json_trans[-10:] # get last 10 transactions

        tran_ids = []
        tran_types = []
        tran_amounts = []
        tran_dates = []
        
        for tran in json_trans:
            tran_ids.append(tran['transactionId'])
            tran_types.append(tran['type'])
            tran_amounts.append(tran['amount'])
            tran_dates.append(tran['date'][:10])

        print(tran_dates)

        return render(request, 'expense_app_polls/userpage.html' , {'ids' : tran_ids, 'types':tran_types, 'amounts':tran_amounts, 'dates':tran_dates}) #'Hi ' + first_name  + '<br>' +account_type +'<br>' +account_num )
    else:
        # No backend authenticated the credentials
        return HttpResponse('NOK')

    

    return HttpResponse(response)