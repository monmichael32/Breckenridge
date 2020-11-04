provider "aws" {
 region = "us-east-1"
}

#resource "aws_s3_bucket" "terraform-serverless-breck"{
    #bucket = "terraform-serverless-breck"
    #acl    = "public-read"
#}

resource "aws_lambda_function" "post_avail" {
   function_name = "ServerlessExample"

   # The bucket name as created earlier with "aws s3api create-bucket"
   s3_bucket = "terraform-serverless-breck"
   #s3_key    = "v1.0.0/example.zip"
   s3_key    = "index.zip"

   # "main" is the filename within the zip file (main.js) and "handler"
   # is the name of the property under which the handler function was
   # exported in that file.
   handler = "index.handler"
   runtime = "nodejs10.x"

   role = "arn:aws:iam::930811541552:role/Breckenridge"
}

#user_names = {
  #"YoRobots" = {
    #path          = "/"
    #force_destroy = true
    #tag_email     = "nobody@example.com"
  #}
#}

#resource "aws_iam_role" "lambda_exec" {
   #name = "serverless_example_lambda"
   #arn = "arn:aws:iam:us-east-1:930811541552:role/Breckenridge"
   #assume_role_policy = <<EOF
#{
  #"Version": "2012-10-17",
  #"Statement": [
    #{
      #"Action": "sts:AssumeRole",
      #"Principal": {
        #"Service": "lambda.amazonaws.com"
      #},
#"Effect": "Allow",
      #"Sid": ""
    #}
  #]
#}
#EOF

#}

#resource "aws_iam_user" "user" {
  #for_each = var.user_names

  #name          = each.key
  #path          = each.value["path"]
  #force_destroy = each.value["force_destroy"]

  #tags = "${map("EmailAddress", each.value["tag_email"])}"
#}

#resource "aws_iam_user_group_membership" "group_membership" {
  #for_each = var.group_memberships

  #user   = each.key
  #groups = each.value

  #depends_on = [ aws_iam_user.user ]
#}


resource "aws_api_gateway_resource" "proxy" {
   rest_api_id = aws_api_gateway_rest_api.breck_api_gateway.id
   parent_id   = aws_api_gateway_rest_api.breck_api_gateway.root_resource_id
   path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "proxy" {
   rest_api_id   = aws_api_gateway_rest_api.breck_api_gateway.id
   resource_id   = aws_api_gateway_resource.proxy.id
   http_method   = "ANY"
   authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda" {
   rest_api_id = aws_api_gateway_rest_api.breck_api_gateway.id
   resource_id = aws_api_gateway_method.proxy.resource_id
   http_method = aws_api_gateway_method.proxy.http_method

   integration_http_method = "POST"
   type                    = "AWS_PROXY"
   uri                     = aws_lambda_function.post_avail.invoke_arn
}

resource "aws_api_gateway_method" "proxy_root" {
   rest_api_id   = aws_api_gateway_rest_api.breck_api_gateway.id
   resource_id   = aws_api_gateway_rest_api.breck_api_gateway.root_resource_id
   http_method   = "ANY"
   authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_root" {
   rest_api_id = aws_api_gateway_rest_api.breck_api_gateway.id
   resource_id = aws_api_gateway_method.proxy_root.resource_id
   http_method = aws_api_gateway_method.proxy_root.http_method

   integration_http_method = "POST"
   type                    = "AWS_PROXY"
   uri                     = aws_lambda_function.post_avail.invoke_arn
}

resource "aws_lambda_permission" "apigw" {
   statement_id  = "AllowAPIGatewayInvoke"
   action        = "lambda:InvokeFunction"
   function_name = aws_lambda_function.post_avail.function_name
   principal     = "apigateway.amazonaws.com"

   # The "/*/*" portion grants access from any method on any resource
   # within the API Gateway REST API.
   source_arn = "${aws_api_gateway_rest_api.breck_api_gateway.execution_arn}/*/*"
}

#variable "app_version" {
#}

