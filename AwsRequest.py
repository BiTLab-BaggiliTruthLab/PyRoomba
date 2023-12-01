import requests, datetime, hashlib, hmac

#Authentiction : aws4-hmac-sha256

class AwsRequest:
    def __init__(self, region, access_key, secret_key, session_token, service):
        self.region = region
        self.access_key = access_key
        self.secret_key = secret_key
        self.session_token = session_token
        self.service = service

    #Return signature using HMAC-SHA256 from key + msg
    def sign(self, key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()
    
    #Generate AWS4-HMAC-SHA256 signing key from key,date stamp, region, and service name
    def generate_signature_key(self, key, dateStamp, regionName, serviceName):
        key_date = self.sign(('AWS4' + key).encode('utf-8'), dateStamp)
        key_region = self.sign(key_date, regionName)
        key_service = self.sign(key_region, serviceName)
        key_sign = self.sign(key_service, 'aws4_request')
        return key_sign

    def get(self, host, uri, query=""):

        method = "GET"
        timenow = datetime.datetime.utcnow() #Current UTC timenow
        amzdate = timenow.strftime('%Y%m%dT%H%M%SZ') #Datetime headers
        datestamp = timenow.strftime('%Y%m%d') # Datetime credential scope

        canonical_uri = uri 
        canonical_querystring = query
        canonical_headers = 'host:' + host + '\n' + 'x-amz-date:' + amzdate + '\n' + 'x-amz-security-token:' + self.session_token + '\n'
        
        signed_headers = 'host;x-amz-date;x-amz-security-token'
        payload_hash = hashlib.sha256(('').encode('utf-8')).hexdigest()
        canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash

        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = datestamp + '/' + self.region + '/' + self.service + '/' + 'aws4_request'
        string_to_sign = algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

        signing_key = self.generate_signature_key(self.secret_key, datestamp, self.region, self.service)
        signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

        authorization_header = algorithm + ' ' + 'Credential=' + self.access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
        headers = {'x-amz-security-token': self.session_token, 'x-amz-date':amzdate, 'Authorization':authorization_header}

        req = "https://%s%s" % (host, uri)
        if query != "":
            req += "?%s" % query
        
        print("request==>", req)
        return requests.get(req, headers=headers)