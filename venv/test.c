#include<stdio.h>
#include<conio.h>

typedef struct list
{
    int info;
    struct list*link;
}node;

node* start;

void create_list()
{
    start=NULL;
}

void insert_at_first(int element)
{
    node* newnode;
    newnode=(node*) malloc(sizeof (node));
    newnode->info=element;
    if (start==NULL)
    {
        newnode->link=NULL;
        start=newnode;
    }
    else
    {
        newnode->link=start;
        start=newnode;
    }
}

void insert_at_end(int element)
{
    node*newnode,*ptr;
    newnode=(node *) malloc(sizeof (node));
    newnode->info=element;
    newnode->link=NULL;
    if(start==NULL)
    {
        start=newnode;
    }
    else
    {
        ptr=start;
        while(ptr->link!=NULL)
        {
            ptr=ptr->link;
        }
        ptr->link=newnode;
    }
}

void insert_after_search(int se,int element)
{
    node*ptr,*newnode;
    ptr=start;
    while(ptr!=NULL)
    {
        if(ptr->info==se)
        {
            break;
        }
        ptr=ptr->link;
    }
    if(ptr==NULL)
    {
        printf("No Insertion");
    }
    else
    { 
        newnode=(node*) malloc(sizeof (node));
        newnode->info=element;
        newnode->link=ptr->link;
        ptr->link=newnode;
    }
}

void delete_first()
{
    if(start==NULL)
    {
        printf("Underflow");
    }
    else
    {
        node* temp = start;
        start = start->link;
        free(temp);
    }
}

void delete_last()
{
    node*ptr,*previous;
    if(start==NULL)
    {
        printf("Underflow");
    }
    else if(start->link==NULL)
    {
        start=NULL;
    }
    else
    {
        ptr=start;
        while(ptr->link->link!=NULL)
        {
            ptr = ptr->link;
        }    
        previous=ptr;
        ptr = previous->link;
        previous->link = NULL;
        free(ptr);
    }
}

void delete_search(int se)
{
    node*ptr,*previous;
    ptr=start;
    while (ptr!=NULL)
    {
        if(ptr->info==se)
        {
            break;
        }
        previous=ptr;
        ptr=ptr->link;
    }
    if(ptr==NULL)
    {
        printf("No Deletion");
    }
    else if(ptr==start)
    {
        start=start->link;
    }
    else
    {
        previous->link=ptr->link;
        free(ptr);
    }
}

void Traversing()
{
    node*ptr;
    ptr=start;
    while(ptr!=NULL)
    {
        printf(" %d", ptr->info);
        ptr=ptr->link;
    }
    printf("\n\n");
}

void main()
{
    int se,element,choice;
    create_list();
    do 
    {
        printf("1.Insert at first\n");
        printf("2.Insert at end\n");
        printf("3.Insert at after search\n");
        printf("4.Delete first\n");
        printf("5.Delete last\n");
        printf("6.Delete searching element\n");
        printf("7.Traversing\n");
        printf("8.Exit\n");
        printf("Enter your choice: ");
        scanf("%d",&choice);
        switch(choice)
        {
        case 1:
            printf("Enter new element: ");
            scanf("%d",&element);
            insert_at_first(element);
            break;
            
        case 2:
            printf("Enter new element: ");
            scanf("%d",&element);
            insert_at_end(element);
            break;

        case 3:
            printf("Enter searching element: ");
            scanf("%d", &se);
            printf("Enter new element: ");
            scanf("%d",&element);
            insert_after_search(se,element);
        break;
        
        case 4:
            delete_first();
            break;

        case 5:
            delete_last();
        break;

        case 6:
            printf("Enter searching element: ");
            scanf("%d",&se);
            delete_search(se);
        break;

        case 7:
            Traversing();
        break;    
        } 
    }while(choice!=8);
}