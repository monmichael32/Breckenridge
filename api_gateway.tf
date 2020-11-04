resource "aws_api_gateway_rest_api" "breck_api_gateway" {
  name        = "Serverless_api"
  description = "Terraform Serverless Application Example"
}

resource "aws_api_gateway_deployment" "breck-deploy" {
   depends_on = [
     aws_api_gateway_integration.lambda,
     aws_api_gateway_integration.lambda_root,
   ]

   rest_api_id = aws_api_gateway_rest_api.breck_api_gateway.id
   stage_name  = "test"
}

output "base_url" {
  value = aws_api_gateway_deployment.breck-deploy.invoke_url
}

