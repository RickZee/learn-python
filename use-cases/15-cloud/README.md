[Home](../../README.md) › [Projects](../README.md) › Cloud and operations

# Cloud and operations

Code that runs on someone else's machines: a function per request, a container, a script that creates infrastructure.

## Tools

- boto3 for AWS
- A Lambda function whose runtime is a current Python, 3.14 for new work
- Docker for the image
- The AWS CDK or a Terraform provider when the infrastructure is code

## Do this first

1. Open [01-lesson.ipynb](01-lesson.ipynb) and run it.
2. Return a different status when the event is missing the field.
3. Keep the change small enough to finish in one sitting.

## Where it sits

The handler is the same shape as a [service](../04-services/README.md) function.

**Next:** [Projects](../README.md)
