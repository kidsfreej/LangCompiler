#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
typedef int DWORD;
typedef struct DataSize DataSize;  
typedef struct List List; 

extern void mains();
DataSize* reprListReal( List* l); 
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
int digitCounter(int a){
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
         DataSize* a = reprListReal(l->values[i]);
         appendList(&tempL,a,3);
         size+=a->size;
         commaCount++;
      }else{
         int nsize =digitCounter(l->values[i]);
         char* t = malloc(nsize);
         itoa(l->values[i],t,10);

         // printf(t);
         DataSize* d = malloc(sizeof(DataSize));
         d->size = nsize;
         d->data = t;
         appendList(&tempL, d,3);
         size+=nsize;
         commaCount++;
      }
   }
   commaCount--;
               // printf("digit%d",size);
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

int main() {
   mains();
   // printf() displays the string inside quotation
   // a();

   // printf("bruh");
   return 0;
}
void print(int a){
   printf("%d\n",a);
}
int input(){
   int inp = 0;
   printf("input:\n");
   scanf("%d",&inp);
   return inp;
}
void error(int a){
   if(a==0){
      printf("Unexpected int\n");
   }else if(a ==1){
      printf("Unexpected bool\n");
   }else if(a==2){
      printf("Unexpected null\n");
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


