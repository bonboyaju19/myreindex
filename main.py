import logger
import handler
from reindex import (background_reindex, wait_for_completed)
import sys

logger = logger.get_logger()
error_type = handler.ErrorType


if __name__ == "__main__":
    '''
    コマンドライン引数で必要な引数を与える!
    python3 main.py JIRA_URL ADMIN_USER ADMIN_PASSWORD
    '''

    logger.info("処理を開始します")

    args = sys.argv  # コマンドライン引数
    try:
        jira_url = args[1].rstrip('/')  # URLから末尾の/を除去
        user = args[2]  # admin user
        password = args[3]  # admin password

        background_reindex(jira_url, user, password)

        wait_for_completed(jira_url, user, password)

        logger.info("処理が完了しました")
    except Exception as e:
        handler.handle_error(error_type.OTHER_UNKNOWN_ERROR, e)
