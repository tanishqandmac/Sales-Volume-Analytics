CALLBACKURL = "https://richilysr.herokuapp.com/webhooks"
GRAPHQL_URL_QUERY = 'https://{}/admin/api/graphql.json'
GRAPHQL_HEADERS_QUERY = '''{{
                'Content-Type': 'application/graphql',
                    'X-Shopify-Access-Token': {},
                    }}
                '''

HEADERS_QUERY = '''{{
                'Content-Type': 'application/json',
                    'X-Shopify-Access-Token': {},
                    }}
                '''

GRAPHQL_TIMEZONE_QUERY = '''
{
  shop{
  email
    timezoneOffset
  }
}
'''

GRAPHQL_WEBHOOK_CHECK_QUERY ='''
{{
  webhookSubscriptions(first:1, callbackUrl:"{}"){{
    edges{{
      node{{
        id
      }}
    }}
  }}
}}
'''
GRAPHQL_WEBHOOK_CHECK_QUERY = GRAPHQL_WEBHOOK_CHECK_QUERY.format(CALLBACKURL + "webhooks")
JSON_WEBHOOK_CREATE_QUERY = {
                  "query": '''
    mutation webhookSubscriptionCreate($topic: WebhookSubscriptionTopic!, $webhookSubscription: WebhookSubscriptionInput!) {
      webhookSubscriptionCreate(topic: $topic, webhookSubscription: $webhookSubscription) {
        userErrors {
          field
          message
        }
        webhookSubscription {
          id
        }
      }
    }
                ''',
                  "variables": {
                    "topic": "ORDERS_CREATE",
                    "webhookSubscription": {"callbackUrl": CALLBACKURL + "webhooks"}
                  }
                }

JSON_WEBHOOK_DESTROY_QUERY = {
                  "query": '''
    mutation webhookSubscriptionCreate($topic: WebhookSubscriptionTopic!, $webhookSubscription: WebhookSubscriptionInput!) {
      webhookSubscriptionCreate(topic: $topic, webhookSubscription: $webhookSubscription) {
        userErrors {
          field
          message
        }
        webhookSubscription {
          id
        }
      }
    }
                ''',
                  "variables": {
                    "topic": "APP_UNINSTALLED",
                    "webhookSubscription": {"callbackUrl": CALLBACKURL + "uninstall"}
                  }
                }

JSON_WEBHOOK_REFUND_QUERY = {
                  "query": '''
    mutation webhookSubscriptionCreate($topic: WebhookSubscriptionTopic!, $webhookSubscription: WebhookSubscriptionInput!) {
      webhookSubscriptionCreate(topic: $topic, webhookSubscription: $webhookSubscription) {
        userErrors {
          field
          message
        }
        webhookSubscription {
          id
        }
      }
    }
                ''',
                  "variables": {
                    "topic": "REFUNDS_CREATE",
                    "webhookSubscription": {"callbackUrl": CALLBACKURL + "refunds"}
                  }
                }

GRAPHQL_PRODUCT_FETCH_QUERY = '''
{{
  orders(first:75 {}) {{
    edges {{
      cursor
      node {{
        id
        createdAt
        lineItems(first: 5) {{
          edges {{
            node {{
            sku
            name
            vendor
            quantity
            }}
          }}
          pageInfo {{
            hasNextPage
          }}
        }}
      }}
    }}
    pageInfo {{
      hasNextPage
    }}
  }}
}}
'''

GRAPHQL_EXTRA_PRODUCTS_FETCH_QUERY = '''
{{
  order(id: "{}") {{
    createdAt
    lineItems(first:200) {{
      edges {{
        cursor
        node {{
          sku
          name
          vendor
          quantity
        }}
      }}
    }}
  }}
}}
'''

GRAPHQL_ORDER_FETCH_QUERY = '''
{{
  orders(first: 100 {}) {{
    edges {{
      cursor
      node {{
        id
        createdAt
        totalPriceSet{{
          shopMoney{{
            amount
          }}
        }}
        totalShippingPriceSet{{
          shopMoney{{
            amount
          }}
        }}
        totalRefundedShippingSet{{
          shopMoney{{
            amount
          }}
        }}
        totalRefundedSet{{
          shopMoney{{
            amount
          }}
        }}
      }}
    }}
    pageInfo {{
      hasNextPage
    }}
  }}
}}
'''
