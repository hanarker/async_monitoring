import azure.functions as func
import azure.durable_functions as df
import logging

async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    logging.info('Durable HTTP trigger function processed a request.')

    client = df.DurableOrchestrationClient(starter)
    instance_id = await client.start_new("async_orchestrator", None)

    return func.HttpResponse(
        body=f'{{"job_id": "{instance_id}"}}',
        status_code=202,
        mimetype="application/json"
    )