CALLBACKURL = "https://cfff8fe3.ngrok.io/webhooks"
GRAPHQL_URL_QUERY = 'https://{}/admin/api/graphql.json'
GRAPHQL_HEADERS_QUERY = '''{{
                'Content-Type': 'application/graphql',
                    'X-Shopify-Access-Token': {},
                    }}'''

HEADERS_QUERY = '''{{
                'Content-Type': 'application/json',
                    'X-Shopify-Access-Token': {},
                    }}'''

GRAPHQL_WEBHOOK_CHECK_QUERY = '''
{
  webhookSubscriptions(first:1, callbackUrl:"https://cfff8fe3.ngrok.io/webhooks"){
    edges{
      node{
        id
      }
    }
  }
}
'''

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
                    "webhookSubscription": {"callbackUrl": CALLBACKURL}
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
                    "webhookSubscription": {"callbackUrl": "https://cfff8fe3.ngrok.io/uninstall"}
                  }
                }

GRAPHQL_ORDER_FETCH_QUERY = '''
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

GRAPHQL_EXTRA_ORDERS_FETCH_ORDERS = '''
{{
  order(id: "{}") {{
    createdAt
    lineItems(first:200) {{
      edges {{
        cursor
        node {{
          sku
          name
          quantity
        }}
      }}
    }}
  }}
}}
'''
