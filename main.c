#include <stdio.h>
#include <string.h>
#include <windows.h>
#include <sql.h>
#include <sqlext.h>
#include <sqltypes.h>
#include <stdbool.h>
#include <stdlib.h>
#include <malloc.h>
#include "Equipments.h"

SQLRETURN ret;       // ODBC 函数返回值
SQLHENV henv = SQL_NULL_HENV;   // 环境句柄
SQLHDBC hdbc = SQL_NULL_HDBC;   // 连接句柄
SQLHSTMT hstmt = SQL_NULL_HSTMT;// 语句句柄

static Node* lastSavedNode = NULL; // 记录上次保存位置

Node* CreateNode() {
    Node* node = (Node*)malloc(sizeof(Node));
    if (node == NULL) {
        printf("内存分配失败\n");
        exit(1);
    }
    node->next = NULL;
    return node;
}

void initList(List* list) {
    list->front = NULL;
    list->size = 0;
}

// ODBC 连接函数
void Connect() {
    henv = SQL_NULL_HENV;
    hdbc = SQL_NULL_HDBC;
    hstmt = SQL_NULL_HSTMT;

    //  分配环境句柄
    ret = SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &henv);
    if (!SQL_SUCCEEDED(ret)) {
        printf("SQLAllocHandle(ENV) 失败，错误码: %d\n", ret);
        return;
    }

    //  设置 ODBC 版本（ODBC3）
    ret = SQLSetEnvAttr(henv, SQL_ATTR_ODBC_VERSION, (void*)SQL_OV_ODBC3, SQL_IS_INTEGER);
    if (!SQL_SUCCEEDED(ret)) {
        printf("SQLSetEnvAttr 失败，错误码: %d\n", ret);
        SQLFreeHandle(SQL_HANDLE_ENV, henv); // 释放环境句柄
        henv = SQL_NULL_HENV;
        return;
    }

    //  分配连接句柄
    ret = SQLAllocHandle(SQL_HANDLE_DBC, henv, &hdbc);
    if (!SQL_SUCCEEDED(ret)) {
        printf("SQLAllocHandle(DBC) 失败，错误码: %d\n", ret);
        SQLFreeHandle(SQL_HANDLE_ENV, henv); // 释放环境句柄
        henv = SQL_NULL_HENV;
        return;
    }

    // 连接数据库
    ret = SQLConnect(hdbc,
        (unsigned char*)"Equipments", SQL_NTS,
        (unsigned char*)"sa", SQL_NTS,
        (unsigned char*)"", SQL_NTS);
    if (!(ret == SQL_SUCCESS || ret == SQL_SUCCESS_WITH_INFO)) {
        printf("SQLConnect 失败，错误码: %d\n", ret);
        // 释放已分配的连接和环境句柄
        SQLFreeHandle(SQL_HANDLE_DBC, hdbc);
        hdbc = SQL_NULL_HDBC;
        SQLFreeHandle(SQL_HANDLE_ENV, henv);
        henv = SQL_NULL_HENV;
        return;
    }

    //  分配语句句柄
    ret = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
    if (!SQL_SUCCEEDED(ret)) {
        printf("SQLAllocHandle(STMT) 失败，错误码: %d\n", ret);
        // 断开连接并释放句柄
        SQLDisconnect(hdbc);
        SQLFreeHandle(SQL_HANDLE_DBC, hdbc);
        hdbc = SQL_NULL_HDBC;
        SQLFreeHandle(SQL_HANDLE_ENV, henv);
        henv = SQL_NULL_HENV;
        return;
    }
}

// ODBC 资源释放函数：仅释放有效句柄，避免空指针
void Free() {
    // 释放语句句柄
    if (hstmt != SQL_NULL_HSTMT) {
        SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
        hstmt = SQL_NULL_HSTMT;
    }

    // 断开连接并释放连接句柄
    if (hdbc != SQL_NULL_HDBC) {
        SQLDisconnect(hdbc);
        SQLFreeHandle(SQL_HANDLE_DBC, hdbc);
        hdbc = SQL_NULL_HDBC;
    }

    //  释放环境句柄（若有效）
    if (henv != SQL_NULL_HENV) {
        SQLFreeHandle(SQL_HANDLE_ENV, henv);
        henv = SQL_NULL_HENV;
    }
}

// 从数据库加载设备到链表
void loadEquipmentFromDatabase(List* list) {
    Connect(); 

    if (hdbc == SQL_NULL_HDBC) { 
        printf("连接数据库失败，无法加载数据!\n");
        Free();
        return;
    }

    // 查询语句
    SQLPrepare(hstmt, (SQLCHAR*)"SELECT number, E_type, E_name, price, inDate, isBad, badDate FROM Equipments.dbo.Equipments", SQL_NTS);
    ret = SQLExecute(hstmt);

    if (ret == SQL_SUCCESS || ret == SQL_SUCCESS_WITH_INFO) {
        SQLBIGINT number, inDate, badDate;
        SQLDOUBLE price;
        SQLCHAR E_type[50], E_name[50];
        SQLINTEGER isBad;
        SQLLEN len1, len2, len3, len4, len5, len6, len7;

        while (SQLFetch(hstmt) != SQL_NO_DATA) {
            // 获取数据
            ret = SQLGetData(hstmt, 1, SQL_C_SBIGINT, &number, 0, &len1);
            ret = SQLGetData(hstmt, 2, SQL_C_CHAR, E_type, sizeof(E_type), &len2);
            ret = SQLGetData(hstmt, 3, SQL_C_CHAR, E_name, sizeof(E_name), &len3);
            ret = SQLGetData(hstmt, 4, SQL_C_DOUBLE, &price, 0, &len4);
            ret = SQLGetData(hstmt, 5, SQL_C_SBIGINT, &inDate, 0, &len5);
            ret = SQLGetData(hstmt, 6, SQL_C_SLONG, &isBad, 0, &len6);
            ret = SQLGetData(hstmt, 7, SQL_C_SBIGINT, &badDate, 0, &len7);

            // 创建链表节点并填充数据
            Node* newNode = CreateNode();
            newNode->que.number = number;
            strncpy_s(newNode->que.type, sizeof(newNode->que.type), (const char*)E_type, _TRUNCATE);
            strncpy_s(newNode->que.name, sizeof(newNode->que.name), (const char*)E_name, _TRUNCATE);
            newNode->que.price = price;
            newNode->que.inDate = inDate;
            newNode->que.isBad = isBad;
            newNode->que.badDate = badDate;

            // 插入链表头部
            newNode->next = list->front;
            list->front = newNode;
            list->size++;
        }
    }
    else {
        printf("加载数据失败，错误码: %d\n", ret);
    }

    lastSavedNode = list->front; // 记录初始保存位置
    Free(); // 释放 ODBC 资源
}

// 将链表新设备保存到数据库（仅保存未同步的节点）
void saveEquipmentToDatabase(List* list) {
    Connect(); 

    if (hdbc == SQL_NULL_HDBC) { 
        printf("连接数据库失败，无法保存数据!\n");
        Free();
        return;
    }

    if (lastSavedNode == list->front) { 
        printf("没有新设备需要保存到数据库\n");
        Free();
        return;
    }

    Node* curNode = list->front;
    int savedCount = 0;

    while (curNode != lastSavedNode && curNode != NULL) {
        // 准备插入 SQL 语句
        SQLCHAR sqlStatement[256];
        snprintf((char*)sqlStatement, sizeof(sqlStatement),
            "INSERT INTO Equipments.dbo.Equipments (number, E_type, E_name, price, inDate, isBad, badDate) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)");

        ret = SQLPrepare(hstmt, sqlStatement, SQL_NTS);
        if (!SQL_SUCCEEDED(ret)) {
            printf("SQLPrepare 失败，错误码: %d\n", ret);
            curNode = curNode->next;
            continue;
        }

        //  绑定参数 1: number (BIGINT) 
        SQLLEN numLen = 0;
        ret = SQLBindParameter(hstmt, 1, SQL_PARAM_INPUT,
            SQL_C_SBIGINT, SQL_BIGINT, 0, 0,
            &curNode->que.number, 0, &numLen);
        if (!SQL_SUCCEEDED(ret)) {
            printf("绑定参数1失败，错误码: %d\n", ret);
            SQLFreeStmt(hstmt, SQL_CLOSE);
            curNode = curNode->next;
            continue;
        }

        //  绑定参数 2: E_type (CHAR(32)) 
        SQLLEN typeLen = SQL_NTS; // 字符串以空字符结尾
        ret = SQLBindParameter(hstmt, 2, SQL_PARAM_INPUT,
            SQL_C_CHAR, SQL_CHAR, 32, 0,
            curNode->que.type, 0, &typeLen);
        if (!SQL_SUCCEEDED(ret)) {
            printf("绑定参数2失败，错误码: %d\n", ret);
            SQLFreeStmt(hstmt, SQL_CLOSE);
            curNode = curNode->next;
            continue;
        }

        //  绑定参数 3: E_name (CHAR(32)) 
        SQLLEN nameLen = SQL_NTS;
        ret = SQLBindParameter(hstmt, 3, SQL_PARAM_INPUT,
            SQL_C_CHAR, SQL_CHAR, 32, 0,
            curNode->que.name, 0, &nameLen);
        if (!SQL_SUCCEEDED(ret)) {
            printf("绑定参数3失败，错误码: %d\n", ret);
            SQLFreeStmt(hstmt, SQL_CLOSE);
            curNode = curNode->next;
            continue;
        }

        // 绑定参数 4: price (DOUBLE) 
        SQLLEN priceLen = 0;
        ret = SQLBindParameter(hstmt, 4, SQL_PARAM_INPUT,
            SQL_C_DOUBLE, SQL_DOUBLE, 0, 0,
            &curNode->que.price, 0, &priceLen);
        if (!SQL_SUCCEEDED(ret)) {
            printf("绑定参数4失败，错误码: %d\n", ret);
            SQLFreeStmt(hstmt, SQL_CLOSE);
            curNode = curNode->next;
            continue;
        }

        //  绑定参数 5: inDate (BIGINT) 
        SQLLEN inDateLen = 0;
        ret = SQLBindParameter(hstmt, 5, SQL_PARAM_INPUT,
            SQL_C_SBIGINT, SQL_BIGINT, 0, 0,
            &curNode->que.inDate, 0, &inDateLen);
        if (!SQL_SUCCEEDED(ret)) {
            printf("绑定参数5失败，错误码: %d\n", ret);
            SQLFreeStmt(hstmt, SQL_CLOSE);
            curNode = curNode->next;
            continue;
        }

        // 绑定参数 6: isBad (INT) 
        SQLLEN isBadLen = 0;
        ret = SQLBindParameter(hstmt, 6, SQL_PARAM_INPUT,
            SQL_C_SLONG, SQL_INTEGER, 0, 0,
            &curNode->que.isBad, 0, &isBadLen);
        if (!SQL_SUCCEEDED(ret)) {
            printf("绑定参数6失败，错误码: %d\n", ret);
            SQLFreeStmt(hstmt, SQL_CLOSE);
            curNode = curNode->next;
            continue;
        }

        //  绑定参数 7: badDate (BIGINT 或 NULL) 
        SQLLEN badDateLen = 0;
        void* badDatePtr = &curNode->que.badDate;

        ret = SQLBindParameter(hstmt, 7, SQL_PARAM_INPUT,
            SQL_C_SBIGINT, SQL_BIGINT, 0, 0,
            badDatePtr, 0, &badDateLen);
        if (!SQL_SUCCEEDED(ret)) {
            printf("绑定参数7失败，错误码: %d\n", ret);
            SQLFreeStmt(hstmt, SQL_CLOSE);
            curNode = curNode->next;
            continue;
        }

        // 执行插入操作
        ret = SQLExecute(hstmt);
        if (SQL_SUCCEEDED(ret)) {
            printf("成功保存设备: %llu\n", curNode->que.number);
            savedCount++;
        }
        else {
            printf("插入数据失败: 设备编号 %llu，错误码: %d\n", curNode->que.number, ret);
        }

        // 清理语句句柄（关闭、解绑、重置参数）
        SQLFreeStmt(hstmt, SQL_CLOSE);
        SQLFreeStmt(hstmt, SQL_UNBIND);
        SQLFreeStmt(hstmt, SQL_RESET_PARAMS);

        curNode = curNode->next; // 处理下一个节点
    }

    SQLTransact(henv, hdbc, SQL_COMMIT); // 提交事务
    lastSavedNode = list->front; // 更新上次保存位置
    printf("成功保存 %d 个设备到数据库\n", savedCount);
    Free(); // 释放 ODBC 资源
}

void deleteEquipmentFromDatabase(unsigned long long number) {
    Connect(); // 尝试连接数据库

    if (hdbc == SQL_NULL_HDBC) { // 连接失败则直接返回
        printf("连接数据库失败，无法删除数据!\n");
        Free(); // 确保先释放已分配的句柄（如果有的话）
        return;
    }

    // 准备删除 SQL 语句
    SQLCHAR sqlStatement[256];
    snprintf((char*)sqlStatement, sizeof(sqlStatement),
        "DELETE FROM Equipments.dbo.Equipments WHERE number = ?");

    ret = SQLPrepare(hstmt, sqlStatement, SQL_NTS);
    if (!SQL_SUCCEEDED(ret)) {
        printf("SQLPrepare 失败，错误码: %d\n", ret);
        Free();
        return;
    }

    // 绑定参数: number (BIGINT)
    SQLLEN numLen = 0;
    ret = SQLBindParameter(hstmt, 1, SQL_PARAM_INPUT,
        SQL_C_SBIGINT, SQL_BIGINT, 0, 0,
        &number, 0, &numLen);
    if (!SQL_SUCCEEDED(ret)) {
        printf("绑定参数失败，错误码: %d\n", ret);
        Free();
        return;
    }

    // 执行删除操作
    ret = SQLExecute(hstmt);
    if (SQL_SUCCEEDED(ret)) {
        SQLLEN rowsAffected = 0;
        SQLRowCount(hstmt, &rowsAffected);
        if (rowsAffected > 0) {
            printf("成功从数据库删除设备: %llu\n", number);
        }
        else {
            printf("数据库中没有找到编号为 %llu 的设备\n", number);
        }
    }
    else {
        printf("删除数据失败: 设备编号 %llu，错误码: %d\n", number, ret);
    }

    SQLTransact(henv, hdbc, SQL_COMMIT); // 提交事务
    Free(); // 正确释放所有句柄
}

// 更新数据库中的设备信息
void updateEquipmentInDatabase(Equipment* equipment) {
    Connect(); // 尝试连接数据库

    if (hdbc == SQL_NULL_HDBC) { // 连接失败则直接返回
        printf("连接数据库失败，无法更新数据!\n");
        Free();
        return;
    }

    // 准备更新 SQL 语句
    SQLCHAR sqlStatement[512];
    snprintf((char*)sqlStatement, sizeof(sqlStatement),
        "UPDATE Equipments.dbo.Equipments "
        "SET E_type = ?, E_name = ?, price = ?, inDate = ?, isBad = ?, badDate = ? "
        "WHERE number = ?");

    ret = SQLPrepare(hstmt, sqlStatement, SQL_NTS);
    if (!SQL_SUCCEEDED(ret)) {
        printf("SQLPrepare 失败，错误码: %d\n", ret);
        Free();
        return;
    }

    // 绑定参数 
    SQLLEN typeLen = SQL_NTS;
    ret = SQLBindParameter(hstmt, 1, SQL_PARAM_INPUT,
        SQL_C_CHAR, SQL_CHAR, 32, 0,
        equipment->type, 0, &typeLen);

    SQLLEN nameLen = SQL_NTS;
    ret = SQLBindParameter(hstmt, 2, SQL_PARAM_INPUT,
        SQL_C_CHAR, SQL_CHAR, 32, 0,
        equipment->name, 0, &nameLen);

    SQLLEN priceLen = 0;
    ret = SQLBindParameter(hstmt, 3, SQL_PARAM_INPUT,
        SQL_C_DOUBLE, SQL_DOUBLE, 0, 0,
        &equipment->price, 0, &priceLen);

    SQLLEN inDateLen = 0;
    ret = SQLBindParameter(hstmt, 4, SQL_PARAM_INPUT,
        SQL_C_SBIGINT, SQL_BIGINT, 0, 0,
        &equipment->inDate, 0, &inDateLen);

    SQLLEN isBadLen = 0;
    ret = SQLBindParameter(hstmt, 5, SQL_PARAM_INPUT,
        SQL_C_SLONG, SQL_INTEGER, 0, 0,
        &equipment->isBad, 0, &isBadLen);

    SQLLEN badDateLen = 0;
    ret = SQLBindParameter(hstmt, 6, SQL_PARAM_INPUT,
        SQL_C_SBIGINT, SQL_BIGINT, 0, 0,
        &equipment->badDate, 0, &badDateLen);

    SQLLEN numLen = 0;
    ret = SQLBindParameter(hstmt, 7, SQL_PARAM_INPUT,
        SQL_C_SBIGINT, SQL_BIGINT, 0, 0,
        &equipment->number, 0, &numLen);

    // 执行更新操作
    ret = SQLExecute(hstmt);
    if (SQL_SUCCEEDED(ret)) {
        SQLLEN rowsAffected = 0;
        SQLRowCount(hstmt, &rowsAffected);
        if (rowsAffected > 0) {
            printf("成功更新数据库中的设备信息: %llu\n", equipment->number);
        }
        else {
            printf("数据库中没有找到编号为 %llu 的设备\n", equipment->number);
        }
    }
    else {
        printf("更新数据失败: 设备编号 %llu，错误码: %d\n", equipment->number, ret);
    }

    SQLTransact(henv, hdbc, SQL_COMMIT); // 提交事务
    Free(); // 释放 ODBC 资源
}

int main(int argc, char* argv[]) {
    List list;
    initList(&list);
    loadEquipmentFromDatabase(&list); // 程序启动时从数据库加载设备

    bool isRun = true;
    while (isRun) {
        switch (menu()) {
        case Quit:
            isRun = false;
            break;

        case Entry:
            entryEquipment(&list);    // 录入设备到链表
            saveEquipmentToDatabase(&list); // 链表新设备同步到数据库
            break;

        case Print:
            printEquipment(&list);   // 打印链表设备
            break;

        case Save:
            saveEquipment(&list);    // 链表设备保存到本地文件
            break;

        case Static:
            staticEquipment(&list);  // 统计链表设备数量
            break;

        case Find: {
            Node* node = findEquipment(&list); // 查询设备
            if (!node) {
                printf_s("对不起，没有找到该设备\n");
            }
            else {
                printf_s("  *  编号  类型   名称   价格   购入时间   是否损坏  损坏时间*\n");
                printf_s("%llu | %s | %s | %.3f | %llu | %d | %llu\n",
                    node->que.number, node->que.type, node->que.name,
                    node->que.price, node->que.inDate, node->que.isBad,
                    node->que.badDate);
            }
            break;
        }

        case Alter:
            alterEuipment(&list);    // 修改链表设备信息
            break;

        case Delete:
            deleteEquipment(&list); // 删除链表设备
            break;

        case AddNULL:
            add(&list);
            saveEquipmentToDatabase(&list);
            break;

        default:
            printf_s("请重新输入\n");
        }

        if (isRun) {
            system("pause");  // 暂停以便查看结果
            system("cls");    // 清屏准备下一次操作
        }
    }

    return 0;
}