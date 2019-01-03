from . import HEADERS_QUERY, JSON_WEBHOOK_CREATE_QUERY, GRAPHQL_URL_QUERY, GRAPHQL_WEBHOOK_CHECK_QUERY, GRAPHQL_ORDER_FETCH_QUERY, CALLBACKURL, GRAPHQL_HEADERS_QUERY, JSON_WEBHOOK_DESTROY_QUERY, GRAPHQL_EXTRA_ORDERS_FETCH_ORDERS
from django.views.decorators.csrf import csrf_exempt
from shopify_auth.decorators import login_required
from .models import UserDatabase,ProductsDatabase
from shopify_webhook.decorators import webhook
from shopify_auth.models import AbstractShopUser
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib import auth
from operator import itemgetter
from collections import Counter
from datetime import datetime
from .dateCal import datePicker,summaryPicker
import traceback
import requests
import shopify
import time
import os

@csrf_exempt
@webhook
def orders_create(request):
    try:
        userObject = UserDatabase.objects.get(domainName = str((request.webhook_domain)).split(".")[0])
        data = request.webhook_data
        for a in data['line_items']:
            if (a['sku']==""):
                sku = 0
            else:
                sku = a['sku']
            productsList = ProductsDatabase(sno = userObject,sku = sku, productName = str(a['name']),quantity = int(a['quantity']),createdAt = data['created_at'].split("T")[0])
            productsList.save()
        return HttpResponse('200')
    except BaseException as e:
        return HttpResponse('404')

@csrf_exempt
@webhook
def app_uninstalled(request):
    try:
        data = request.webhook_data
        UserDatabase.objects.filter(domainName = str(data['domain']).split(".")[0]).delete()
        return HttpResponse('200')
        del request.user.session
    except Exception:
        print(traceback.format_exc())
        return HttpResponse('404')

@login_required
def index(request, *args, **kwargs):
    with request.user.session:
        try:
            print (request.user)
            userObject = UserDatabase.objects.get(domainName = str((request.user)).split(".")[0])
            date = request.GET.get('query', '')
            if(date==''):
                productsList = ProductsDatabase.objects.filter(sno = userObject)
                print (len(productsList))
                if(len(productsList)==0):
                    return render(request, "core/sync.html", {})
            else:
                dates = datePicker(date)
                if (len(dates) == 1):
                    print (dates)
                    productsList = ProductsDatabase.objects.filter(sno = userObject,
                                                                createdAt=dates[0])
                    print (len(productsList))
                elif (len(dates) == 2):
                    productsList = ProductsDatabase.objects.filter(sno = userObject,
                                                                createdAt__range=(dates[0], dates[1]))
            pList = ProductsDictMaker(userObject,productsList)
            Summary = summaryPicker(date)
            return render(request, "core/report.html", {'Products': pList, "Summary":Summary})
        except Exception:
            print(traceback.format_exc())
            return render(request, "core/sync.html", {})

@login_required
def sync(request, *args, **kwargs):
    with request.user.session:
        try:
            #Local Variables Decl.
            queryData = ""
            Products = []
            customProducts = []
            domain_name = request.user
            user_token = request.user.token

            #Headers
            graphql_headers = {
            'Content-Type': 'application/graphql',
                'X-Shopify-Access-Token': user_token,
                }
            headers = {
                'Content-Type': 'application/json',
                'X-Shopify-Access-Token': user_token ,
                }

            #Recreating User Object
            userObject = UserDatabase.objects.filter(domainName = str((request.user)).split(".")[0]).delete()
            userObject = UserDatabase(domainName = str((request.user)).split(".")[0],lastModified = datetime.now())
            userObject.save()

            #Graphql Query for Checking Webhook Existence
            r = requests.post(GRAPHQL_URL_QUERY.format(domain_name),
            headers = graphql_headers,data = GRAPHQL_WEBHOOK_CHECK_QUERY)
            response = r.json()
            if not response['data']['webhookSubscriptions']['edges']:
                response1 = requests.post(GRAPHQL_URL_QUERY.format(domain_name),
                                        headers = headers,
                                        json = JSON_WEBHOOK_CREATE_QUERY)
                response2 = requests.post(GRAPHQL_URL_QUERY.format(domain_name),
                                        headers = headers,
                                        json = JSON_WEBHOOK_DESTROY_QUERY)

            #Fetching Orders and Storing them via Graphql
            response = requests.post(GRAPHQL_URL_QUERY.format(domain_name),
                                    headers=graphql_headers,
                                    data=GRAPHQL_ORDER_FETCH_QUERY.format(""))

            responseJSON = response.json()
            GrossSales = GrossSalesCal(userObject,responseJSON,customProducts)
            k = 2
            while(GrossSales[0]!=0):
                if(GrossSales[0] == 1):
                    dataH = GRAPHQL_ORDER_FETCH_QUERY.format(", after:" + "\"" + GrossSales[1] + "\"")
                    response = requests.post(GRAPHQL_URL_QUERY.format(domain_name),
                                            headers = graphql_headers,
                                            data = dataH)
                    responseJSON = response.json()
                    myList = GrossSales[2]
                    GrossSales = GrossSalesCal(userObject,responseJSON,GrossSales[2])
                    k = 2
                    time.sleep(1)
                    print ("1 - " + str(k))
                elif(GrossSales[0] == -1):
                    time.sleep(2**k)
                    response = requests.post(GRAPHQL_URL_QUERY.format(domain_name),
                                            headers = graphql_headers,
                                            data = dataH)
                    responseJSON = response.json()
                    GrossSales = GrossSalesCal(userObject,responseJSON,myList)
                    k += 1
                    print ("-1 - " + str(k))

            print ("Done")
            for items in GrossSales[2]:
                print (items)
                response = requests.post(GRAPHQL_URL_QUERY.format(domain_name),
                                        headers = graphql_headers,
                                        data = GRAPHQL_EXTRA_ORDERS_FETCH_ORDERS.format(items))
                responseJSON = response.json()
                print (responseJSON)
                response = GrossSalesExtraCal(userObject,responseJSON)
                print (response)
                while (response == -1):
                    time.sleep(5)
                    response = requests.post(GRAPHQL_URL_QUERY.format(domain_name),
                                            headers = graphql_headers,
                                            data = GRAPHQL_EXTRA_ORDERS_FETCH_ORDERS.format(items))
                    responseJSON = response.json()
                    response = GrossSalesExtraCal(userObject,responseJSON)

            productsList = ProductsDatabase.objects.filter(sno = userObject)
            pList = ProductsDictMaker(userObject,productsList)

        except Exception:
            print(traceback.format_exc())
            return render(request,"core/error.html",{})
    return redirect('core:index')

def GrossSalesCal(userObject,response,customProductsList):
    try:
        for nodes in response['data']['orders']['edges']:
            if(nodes['node']['lineItems']['pageInfo']['hasNextPage']==False):
                for items in nodes['node']['lineItems']['edges']:
                    try:
                        if (items['node']['sku']=='' or items['node']['sku']==None):
                            SKU = 0
                        else:
                            SKU = int(items['node']['sku'])
                        productsList = ProductsDatabase(sno = userObject,
                                                        sku = SKU,
                                                        productName = str(items['node']['name']),
                                                        quantity = int(items['node']['quantity']),
                                                        createdAt = str(nodes['node']['createdAt']).split("T")[0])
                        productsList.save()
                    except BaseException as e:
                        print (e)
                        continue
            else:
                customProductsList.append(nodes['node']['id'])
        if (response['data']['orders']['pageInfo']['hasNextPage'] == True):
            return [1,response['data']['orders']['edges'][-1]['cursor'],customProductsList]
        else:
            return [0,"-",customProductsList]
    except:
        if(response['errors'][0]['message'] == "Throttled"):
            return [-1]

def GrossSalesExtraCal(userObject,response):
    try:
        for nodes in response['data']['order']['lineItems']['edges']:
            try:
                if (nodes['node']['sku']=='' or nodes['node']['sku']==None):
                    SKU = 0
                else:
                    SKU = int(nodes['node']['sku'])
                productsList = ProductsDatabase(sno = userObject,
                                                sku = SKU,
                                                productName = str(nodes['node']['name']),
                                                quantity = int(nodes['node']['quantity']),
                                                createdAt = str(response['data']['order']['createdAt']).split("T")[0])
                productsList.save()
            except BaseException as e:
                print (e)
                continue
        return (1)
    except:
        if(response['errors'][0]['message'] == "Throttled"):
            return (-1)

def ProductsDictMaker(userObject,productsList):
    plist = []
    distinctProducts = productsList.values_list("sku","productName").distinct()
    for a in distinctProducts:
        quantity = productsList.filter(productName = a[1]).aggregate(Sum('quantity'))
        try:
            b = str(a[1]).split(" - ")
            name = b[0]
            if (len(b[1]) <= 3):
                variant = b[1].upper()
            else:
                variant = b[1].title()
        except:
            name = a[1]
            variant = "-"
        #date = str(distinctProductsFilter[0].createdAt).split()[0]
        plist.append({'SKU':a[0],'Name':name.title(),'Variant':variant,'Quantity':quantity['quantity__sum']})
    #pListSorted = sorted(plist, key=itemgetter('Quantity'), reverse=True)
    return (plist)
