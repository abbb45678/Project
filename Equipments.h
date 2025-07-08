#pragma once
#include<stdbool.h>

/**
* 设备信息
*/
typedef struct Equipment
{
	unsigned long long number;
	char type[32];
	char name[32];
	double price;
	unsigned long long inDate;
	int isBad;
	unsigned long long badDate;

}Equipment;

/*
* 节点Node
*/
typedef struct Node
{
	Equipment que;
	struct Node* next;
}Node;

/**
* 链表
*/
typedef struct List
{
	Node* front;
	int size;
}List;

/**
* 菜单功能
*/
typedef enum MenuOptions
{
	Quit,     //退出
	Entry,    //录入
	Print,    //打印
	Save,     //保存
	Static,   //统计
	Find,     //查询
	Alter,    //修改
	Delete,   //删除
	AddNULL  //添加空设备
}MenuOptions;

/**
* 打印菜单，提供用户选择
*/
int menu();

/**
* 设备录入
*/
void entryEquipment(List* list);

//检测输入是否非法
bool test_num(int result);

//查询编号是否重复
bool isNumberExist(List* list, unsigned long long number);

//遍历字符串
int isInteger(const char* str);

/*
* 设备分类选择
* void choseEquipment( );
*/

//添加空设备
void add(List* list);

//检测是否继续修改
bool ifConAlter();

/**
* 打印信息
*/
void printEquipment(List* list);

/**
* 保存设备信息
*/
void saveEquipment(List* list);


/**
* 统计设备
*/
void staticEquipment(List* list);

/**
* 查找设备
*/
Node* findEquipment(List* list);

/*
*修改设备信息
*/
void alterEuipment(List* list);

/**
* 删除设备
*/
//void deleteEquipment(List* list);
void deleteEquipment(List* list);

/**
* 从数据库删除设备
*/
void deleteEquipmentFromDatabase(unsigned long long number);

/**
* 更新数据库中的设备信息
*/
void updateEquipmentInDatabase(Equipment* equipment);