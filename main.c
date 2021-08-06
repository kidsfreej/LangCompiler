#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
typedef int DWORD;
typedef struct DataSize DataSize;  
typedef struct List List; 
typedef struct Node Node; 
typedef struct LinkedList LinkedList; 
typedef struct Hashmap Hashmap;


typedef void(*func_ptr_t)();




extern void inits();
DataSize* reprListReal( List* l);


struct Node;
struct List{
   int length;
   int trueLength;
   DWORD* values;
   DWORD* types;
};
struct DataSize{
  int size;
  char* data; 
};

struct LinkedList{
   Node* head;
   Node* tail;
};
struct Node{
   Node* next;
   char* key;
   DWORD* value;
   DWORD* type;
};
struct Hashmap{
   LinkedList* map;
   int size;
};

uint32_t hasher(char *key, int len)
{
    uint32_t hash, i;
    for(hash = i = 0; i < len; ++i)
    {
        hash += key[i];
        hash += (hash << 10);
        hash ^= (hash >> 6);
    }
    hash += (hash << 3);
    hash ^= (hash >> 11);
    hash += (hash << 15);
    return hash;
}

void initLinkedList(LinkedList* l){
   l->head = NULL;
   l->tail = NULL;
}
void addLinkedList(LinkedList* l,char* key,DWORD* value,DWORD* type){
   if(l->head==NULL){
      l->head = malloc(sizeof(Node));
      l->tail = l->head;
      l->head->key = key;
      l->head->value = value;
      l->head->type = type;
      return;
   }
   l->tail->next = malloc(sizeof(Node));
   l->tail = l->tail->next;
   l->tail->value = value;
   l->tail->key = key;
   l->tail->type = type;
}
Node* getLinkedList(LinkedList* l,char* key){
   Node* next = l->head;
   while(next!=l->tail->next && next!=NULL){
      if(strcmp(key,next->key)==0){
         return next;
      }
      next = next->next;
   }
   printf("\nError: Nice try but you called a not existant function or property \n");
   return  NULL;
}
void initHashmap(Hashmap* h,int size){
   h->map = malloc(size*sizeof(LinkedList));
   h->size = size;
   for(int i =0;i<size;i++){
      initLinkedList(&h->map[i]);
   }
}

Node* getHashmap(Hashmap* h,char* key,int len){
   uint32_t hashed = hasher(key,len);
   int loc = hashed%h->size;
   return getLinkedList(&h->map[loc],key);
}
void addHashmap(Hashmap* h,char* key,int len,DWORD* value,DWORD* type){
   uint32_t hashed = hasher(key,len);
   int loc = hashed%h->size;
   addLinkedList(&h->map[loc],key,value,type);
}
static Hashmap funcProps;
char* getKeyLen(int func,int type, int funcLen, int len){

   char* toHash = malloc(len+1);
   itoa(func,toHash,10);
   itoa(type,&toHash[funcLen+1],10);
   toHash[funcLen] = '_';
   return toHash;
}
char* getKey(int func,int type){
   int funcLen =  digitCounter(func);
   int len =funcLen+1+digitCounter(type);

   char* toHash = malloc(len+1);
   itoa(func,toHash,10);
   itoa(type,&toHash[funcLen+1],10);
   toHash[funcLen] = '_';
   return toHash;
}
func_ptr_t getHashmapAsm(int func,int type){

   int funcLen =  digitCounter(func);
   int len =funcLen+1+digitCounter(type);
   char* toHash = getKeyLen(func,type,funcLen ,len);
   Node* v= getHashmap(&funcProps,toHash,len);
   free(toHash);
   return (func_ptr_t) v;
}

void initHashmapAsm(int size){
   initHashmap(&funcProps,size);
}
void addHashmapAsm(int func,int otype,DWORD* value,int type){
   int funcLen =  digitCounter(func);
   int len =funcLen+1+digitCounter(otype);
   char* toHash = malloc(len+1);
   itoa(func,toHash,10);
   itoa(otype,&toHash[funcLen+1],10);
   toHash[funcLen] = '_';
   addHashmap(&funcProps,toHash,len,value,type);

}
int digitCounter(int a){
   if(a==0){
      return 1;
   }
   int c = 0;
   if(a<0){
      c= 1;
   }
   return (floor(log10(abs(a)))+1)+c;
}
void initList( List* l){
   l->length = 0;
   l->trueLength = 2;
   l->values = malloc(sizeof(int)*2);
   l->types = malloc(sizeof(int)*2);
}
void appendList( List* l,DWORD value,DWORD type){
   if(l->length==l->trueLength-1){
      l->trueLength*=2;
      DWORD* tempValues =malloc(sizeof(int)*l->trueLength);
      DWORD* tempTypes =malloc(sizeof(int)*l->trueLength);
      for(int i = 0;i<l->length;i++){
         tempValues[i] = l->values[i];
         tempTypes[i] = l->types[i];
      }
      free(l->values);
      free(l->types);
      l->values = tempValues;
      l->types = tempTypes;
   }
   l->values[l->length]= value;
   l->types[l->length] = type;
   l->length++;
}
char* reprList(List* l){
   DataSize* d=  reprListReal(l);
   char* new = malloc(d->size+1);
   strncpy(new,d->data,d->size);
   new[d->size] = '\0';
   free(d->data);
   free(d);
   return new;
}
void freeList(List* l){
   free(l->types);
   free(l->values);
}
void deepfreeList(List* l){
   
   free(l->types);
   free(l->values);
}
DataSize* reprListReal( List* l){
   List tempL;
   int size = 0;
   initList(&tempL);
   
   int commaCount = 0;
   for(int i =0;i<l->length;i++){
      if(l->types[i]==3){
         DataSize* a = reprListReal((List*)l->values[i]);
         appendList(&tempL,(int)a,3);
         size+=a->size;
         commaCount++;
      }else{
         int nsize =digitCounter(l->values[i]);
         char* t = malloc(nsize);
         itoa(l->values[i],t,10);

         DataSize* d = malloc(sizeof(DataSize));
         d->size = nsize;
         d->data = t;
         appendList(&tempL,(int)d,3);
         size+=nsize;
         commaCount++;
      }
   }
   commaCount--;
      // IT ERRORS BELOW HERE >____> IDK

   char* f = malloc(size*sizeof(char)+commaCount*2+2);
   f[0] = '[';
   int inc = 1;
   for(int i=0;i<tempL.length; i++){
      DataSize* td = (DataSize*) tempL.values[i];
      for(int j =0;j<td->size ;j++){

         char v = td->data[j];
         f[inc] = v;
         inc++;
      }
      if(i!=tempL.length-1){
         f[inc] = ',';
         inc++;
         f[inc] = ' ';
         inc++;
      }
      free(td->data);
      free(td);
   }
   f[size*sizeof(char)+commaCount*2+1] = ']';
   DataSize* d = malloc(sizeof(DataSize));
   d->size = size+commaCount*2+2;
   d->data = f;
   return d;
}
void bruh(int a);
int main() {

   initHashmapAsm(7);
   // addHashmap(&funcProps,getKey(5,10),4,bruh);
   // call(5,10)( 5);
   inits();

   return 0;
}
void print(int a){
   printf("%d\n",a);
}
void bruh(int a){
   printf("bruh%d",a);
}
int input(){
   int inp = 0;
   printf("input:\n");
   scanf("%d",&inp);
   return inp;
}
void error(int a){
   if(a==-2){
      printf("Too few parameters");
   }else if (a==-3){
      printf("Too many parameters");
   }
   else if(a==0){
      printf("Unexpected int\n");
   }else if(a ==1){
      printf("Unexpected bool\n");
   }else if(a==2){
      printf("Unexpected null\n");
   }else{
      printf("Unexpected Object and got %d\n",a);
      // char* text = malloc(strlen(name)+13);
      // strcpy(text,"Unexpected ");
      // strcat(text, name);
      // strcat(text, "\n");
      // printf(text);
   }

}
//completely different from malloc
void* mem_alloc(int size){
   void* a = malloc(size);
   if(a==NULL){
      printf("Dumbutt, we have no memory in the heap\n");
   }
   return a;
}


void printstr(char* c){
   printf(c);
}
