import logger
import handler
import requests
import time

logger = logger.get_logger()
error_type = handler.ErrorType


def is_alive(jira_url):
    logger.info("JIRAのステータスチェックを行います")
    try:
        response = requests.get(jira_url + "/status")
        logger.debug(response)
        if response.status_code == 200 and response.json()["state"] == "RUNNING":
            logger.info("ステータスチェックに成功しました:%s" % (response.json()["state"]))
            return True
        else:
            logger.warning("ステータスチェックに失敗しました:%s" % (response.json()["state"]))
            return False
    except Exception as e:
        handler.handle_error(error_type.REINDEX_JIRA_CHECK_FAILED, e)


def background_reindex(jira_url, user, password):
    logger.info("JIRAのバックグラウンドインデックス再作成を行います")
    try:
        if not is_alive(jira_url):
            raise Exception

        response = requests.post(
            jira_url + "/rest/api/2/reindex?type=BACKGROUND", auth=(user, password))
        logger.debug(response)
        if response.status_code == 202:
            logger.info("JIRAのバックグラウンドインデックス再作成が正常に開始しました")
        else:
            handler.handle_error(
                error_type.REINDEX_JIRA_BACKGROUND_REINDEX_START_FAILED)
    except Exception as e:
        handler.handle_error(
            error_type.REINDEX_JIRA_BACKGROUND_REINDEX_FAILED, e)


def is_completed(jira_url, user, password):
    logger.info("JIRAのインデックス再作成の完了を確認します")
    try:
        response = requests.get(
            jira_url + "/rest/api/2/reindex/progress", auth=(user, password))
        logger.debug(response)
        if response.json()["success"] != "true":
            handler.handle_error(error_type.REINDEX_STATUS_FAILED)
        progress = response.json()["currentProgress"]
        if progress == 100:
            logger.info("JIRAのインデックス再作成が完了しました:" + str(progress))
            return True
        else:
            logger.info("JIRAのインデックス再作成の進捗:" + str(progress))
            return False
    except Exception as e:
        handler.handle_error(
            error_type.REINDEX_STATUS_CHECK_FAILED, e)


def wait_for_completed(jira_url, user, password, interval=60, retries=120):
    logger.info("JIRAのインデックス再作成が完了するまで確認します")
    try:
        for r in range(retries):
            if is_completed(jira_url, user, password):
                logger.info("JIRAのインデックス再作成が完了しました")
                return True
            else:
                logger.info("リトライ回数: " + str(r))
                time.sleep(interval)  # 秒
        logger.warning("リトライ回数の上限を超過しました")
        handler.handle_error(error_type.REINDEX_TOO_LONG_TO_COMPLETE)
    except Exception as e:
        handler.handle_error(
            error_type.REINDEX_WAIT_TO_COMPLETED_FAILED, e)
