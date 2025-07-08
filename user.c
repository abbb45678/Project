#include "Equipments.h"
#include<stdio.h>
#include<malloc.h>
#include<string.h>
#include<stdbool.h>

static Node* CreateNode() {
    Node* node = malloc(sizeof(Node));
    if (!node) {
        printf_s("malloc failed!\n");
        return NULL;
    }
    node->next = NULL;
    return node;
}

int menu() {
    printf_s("  ********************************\n");
    printf_s("  *  欢迎使用实验室设备管理系统  *\n");
    printf_s("  ********************************\n");
    printf_s("  *          请选择功能          *\n");
    printf_s("  ********************************\n");
    printf_s("  *       1.录入实验设备         *\n");
    printf_s("  *       2.打印设备信息         *\n");
    printf_s("  *       3.保存设备信息         *\n");
    printf_s("  *       4.统计实验设备         *\n");
    printf_s("  *       5.查询实验设备         *\n");
    printf_s("  *       6.修改设备信息         *\n");
    printf_s("  *       7.删除实验设备         *\n");
    printf_s("  *       8.添加空设备           *\n");
    printf_s("  *       0.退出系统             *\n");
    printf_s("  ********************************\n");
    printf_s("select->");


    int select;
    char check[32] = { 0 };

    if (!test_num(scanf_s("%d", &select)))
    {
        select =100;
    }
    //scanf_s("%c", &check);
    //select = atoi(check);
    //if (!test_num(select))
   // {
     //   return -1;
   // }
    /*
     int select = 100;
     char check[32] = { 0 };
     scanf_s("%c", &check);

     if (isInteger(check))
     {
         select = atoi(check);
         printf_s("%d", select);
         if (!test_num(select))
         {
             return -1;
         }
     }*/



    return select;
}

int isInteger(const char* str) {
    if (str == NULL || *str == '\0') return 0;

    // 允许可选的正负号
    if (*str == '+' || *str == '-') {
        str++;
    }

    // 如果剩下的字符串为空，则不是有效的整数
    if (*str == '\0') return 0;

    // 检查每个字符是否为数字
    while (*str != '\0') {
        if (!isdigit((unsigned char)*str)) {
            return 0;
        }
        str++;
    }

    return 1;
}

bool test_num(int result) {
    if (result != 1) {
        printf("非法输入\n");
        while (getchar() != '\n'); // 清空输入缓冲区
        return 0;
    }
    return 1;
}

void add(List* list)
{
    Node* node = CreateNode();
    node->que.number = 0;
    node->que.type[0] = '\0';
    node->que.name[0] = '\0';
    node->que.price = 0.0;
    node->que.inDate = 0;
    node->que.isBad = 0;
    node->que.badDate = 0;



    // 插入链表头部
    node->next = list->front;
    list->front = node;
    list->size++;

    printf_s("已添加一个空设备节点\n");

}

void entryEquipment(List* list) {
    Node* node = CreateNode();
    bool isRun = true;
    bool E_isRun = true;
    int num;
    unsigned long long E_num;

    while (E_isRun) {
        printf_s("请输入设备编号->");
        if (!test_num(scanf_s("%llu", &E_num))) {
            return; // 修该1：void 函数返回空，而非 return NULL
        }

        if (isNumberExist(list, E_num)) {
            printf_s("该编号已存在，请重新输入!\n");
            continue;
        }
        node->que.number = E_num;

        printf_s("分类：1.测量仪器、2.分析仪器、3.计量仪器、4.制备仪器\n请输入编号->");
        if (!test_num(scanf_s("%d", &num))) {
            return; // 修复2：void 函数返回空
        }

        while (isRun) {
            switch (num) {
            case 1: strcpy_s(node->que.type, sizeof(node->que.type), "测量仪器"); isRun = false; break;
            case 2: strcpy_s(node->que.type, sizeof(node->que.type), "分析仪器"); isRun = false; break;
            case 3: strcpy_s(node->que.type, sizeof(node->que.type), "计量仪器"); isRun = false; break;
            case 4: strcpy_s(node->que.type, sizeof(node->que.type), "制备仪器"); isRun = false; break;
            default:
                printf_s("请重新输入->");
                if (!test_num(scanf_s("%d", &num))) return; // 修复3：void 函数返回空
                continue;
            }
        }

        printf_s("请输入设备名称->");
        if (!test_num(scanf_s("%s", node->que.name, 32))) {
            return; // 修复4：void 函数返回空
        }

        printf_s("请输入设备价格->");
        if (!test_num(scanf_s("%lf", &node->que.price))) {
            return; // 修复5：void 函数返回空
        }

        printf_s("请输入设备购入日期（如20250101）->");
        if (!test_num(scanf_s("%llu", &node->que.inDate))) {
            return; // 修复6：void 函数返回空
        }

        printf_s("1为损坏，0为未损坏\n设备是否损坏->");
        int badNum = -1;
        bool badRun = true;
        while(badRun)
        {
            if (!test_num(scanf_s("%d", &badNum))) {
                return; // 修复7：void 函数返回空
            }

            switch (badNum)
            {
            case 1:
                node->que.isBad = badNum;
                //printf_s("%d", node->que.isBad);
                badRun = false;
                break;
            case 0:
                node->que.isBad = badNum;
                printf_s("%d", node->que.isBad);
                badRun = false;
                break;
            default:
                printf_s("输入错误，请重新输入->\n");
                continue;
            }
        }
            /*
            if (!test_num(scanf_s("%d", &node->que.isBad))) {
                return; // 修复7：void 函数返回空
            }*/

            if (node->que.isBad) {
                printf_s("损坏日期->");
                if (!test_num(scanf_s("%llu", &node->que.badDate))) {
                    return; // 修复8：void 函数返回空
                }
            }
            else {
                node->que.badDate = 0;
            }
       


        // 插入链表头部
        node->next = list->front;
        list->front = node;
        list->size++;
        E_isRun = false;
    }
}

bool isNumberExist(List* list, unsigned long long number) {
    Node* curNode = list->front;
    while (curNode != NULL) {
        if (curNode->que.number == number) {
            return true;
        }
        curNode = curNode->next;
    }
    return false;
}

void printEquipment(List* list) {
    printf_s("  ****************************************************************\n");
    printf_s("  *                  欢迎使用实验室设备管理系统                  *\n");
    printf_s("  ****************************************************************\n");
    printf_s("  *  编号 | 类型 | 名称 | 价格 | 购入时间 | 是否损坏 | 损坏时间  *\n");
    printf_s("  ****************************************************************\n");

    Node* curNode = list->front;
    while (curNode != NULL) {
        printf_s("  *%llu | %s | %s | %.1f | %llu | %d | %llu*\n",
            curNode->que.number, curNode->que.type,
            curNode->que.name, curNode->que.price,
            curNode->que.inDate, curNode->que.isBad,
            curNode->que.badDate);
        curNode = curNode->next;
    }
}

void saveEquipment(List* list) {
    FILE* fp = fopen("Equipments Information", "w");
    if (!fp) {
        perror("file open failed\n");
        return;
    }

    Node* curNode = list->front;
    if (curNode != NULL) {
        fprintf(fp, "%llu | %s | %s | %lf | %llu | %d | %llu\n",
            curNode->que.number, curNode->que.type,
            curNode->que.name, curNode->que.price,
            curNode->que.inDate, curNode->que.isBad,
            curNode->que.badDate);
        printf_s("保存成功!\n");
        curNode = curNode->next;
    }
    else {
        printf_s("没有需要保存的内容！\n");
    }

    fclose(fp);
}

void staticEquipment(List* list) {
    printf_s("设备总数量为：%d\n", list->size);
}

Node* findEquipment(List* list) {
    if (list->size == 0) {
        printf_s("暂无设备\n");
        return NULL;
    }

    char FFind[32] = { 0 };
    printf_s("请输入所查询设备名字或编号->");
    if (!test_num(scanf_s("%s", FFind, 32))) {
        return NULL;
    }

    unsigned long long number = -1;
    int isNumber = sscanf_s(FFind, "%llu", &number) == 1;

    Node* curNode = list->front;
    while (curNode != NULL) {
        if (isNumber) {
            if (curNode->que.number == number) {
                return curNode;
            }
        }
        else {
            if (strcmp(curNode->que.name, FFind) == 0) {
                return curNode;
            }
        }
        curNode = curNode->next;
    }
    return NULL;
}

void alterEuipment(List* list) {
    unsigned long long number;
    printf_s("请输入需修改设备编号->");
    if (!test_num(scanf_s("%llu", &number))) {
        return;
    }

    Node* curNode = list->front;
    while (curNode != NULL) {
        if (curNode->que.number == number) {
            int num = -1;
            bool isRun = true;

            while (isRun) {
                printf_s("1.价格，2.购入日期，3.损坏情况\n请选择需修改信息->");
                if (!test_num(scanf_s("%d", &num))) {
                    return;
                }

                switch (num) {
                case 1:
                    printf_s("请输入要修改的数值->");
                    if (!test_num(scanf_s("%lf", &curNode->que.price))) {
                        return;
                    }
                    printf_s("修改成功\n");
                    updateEquipmentInDatabase(&curNode->que); // 新增：更新数据库
                    if (ifConAlter()) continue;
                    else isRun = false;
                    break;

                case 2:
                    printf_s("请输入要修改的数值->");
                    if (!test_num(scanf_s("%llu", &curNode->que.inDate))) {
                        return;
                    }
                    printf_s("修改成功\n");
                    updateEquipmentInDatabase(&curNode->que); // 心怎：更新数据库
                    if (ifConAlter()) continue;
                    else isRun = false;
                    break;

                case 3:
                    printf_s("1为损坏，0为未损坏\n设备是否损坏->");

                    if (!test_num(scanf_s("%d", &curNode->que.isBad))) {
                        return;
                    }

                  

                    if (curNode->que.isBad) {
                        printf_s("损坏日期->");
                        if (!test_num(scanf_s("%llu", &curNode->que.badDate))) {
                            return;
                        }
                    }
                    else {
                        curNode->que.badDate = 0;
                    }
                    printf_s("修改成功\n");
                    updateEquipmentInDatabase(&curNode->que); // 心怎：更新数据库
                    if (ifConAlter()) continue;
                    else isRun = false;
                    break;

                default:
                    printf_s("请重新输入->");
                    if (!test_num(scanf_s("%d", &num))) return;
                    continue;
                }
            }
            return;
        }
        curNode = curNode->next;
    }

    printf_s("没有找到该设备，修改失败\n");
}

bool ifConAlter() {
    printf_s("是否继续修改(1修改，0不修改)->");
    bool A_num ;
    //int A_num = -1;
    /*
    if (!test_num(scanf_s("%d", &A_num))) {
        return false; // 输入非法时默认不继续
    }
    return A_num ? true : false;*/
    scanf_s("%d", &A_num);
    return A_num;

}

void deleteEquipment(List* list) {
    if (list->size == 0) {
        printf_s("暂无设备\n");
        return;
    }

    // 直接读取数值，避免字符串转换风险
    unsigned long long number;
    printf_s("请输入需删除设备编号->");
    if (!test_num(scanf_s("%llu", &number))) return;

    Node* curNode = list->front;
    Node* prevNode = NULL;

    while (curNode != NULL && curNode->que.number != number) {
        prevNode = curNode;
        curNode = curNode->next;
    }

    if (curNode == NULL) {
        printf_s("未找到设备\n");
        return;
    }

    // 关键修复：正确更新头指针 
    if (prevNode == NULL) {
        list->front = curNode->next;  // 头节点特殊处理
    }
    else {
        prevNode->next = curNode->next;
    }

    deleteEquipmentFromDatabase(curNode->que.number);  // 数据库操作
    free(curNode);
    list->size--;
    printf_s("删除成功！\n");
}                      