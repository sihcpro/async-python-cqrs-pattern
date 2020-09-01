import os


def create_boto3_environment(access_key, access_secret, default_region):

    # Boto3 Document at : https://github.com/boto/boto3
    # Example at: https://realpython.com/python-boto3-aws-s3/

    boto3_root_dir = f"{os.environ['HOME']}/.aws"
    if not os.path.exists(boto3_root_dir):
        os.mkdir(boto3_root_dir)

    with open(os.path.join(boto3_root_dir, "credentials"), "w") as cred:
        cred.write(
            "[default]\n"
            f"aws_access_key_id = {access_key}\n"
            f"aws_secret_access_key = {access_secret}"
        )

    with open(os.path.join(boto3_root_dir, "config"), "w") as config:
        config.write(f"[default]\nregion = {default_region}\n")


def get_s3_url(s3_object) -> str:
    return (
        f"https://{s3_object.bucket_name}.s3-{s3_object.region}.amazonaws.com/"
        f"{s3_object.object_info['Key']}"
    )
