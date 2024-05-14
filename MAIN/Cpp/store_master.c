#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <string.h>

char globe_path[1000] = "";
int globe_ind = 0;
int globe_img_path_ind[100] = {0};
int globe_img_ind = 1;
//const char root_path[] = "/home/ec2-user/stor";
//const char root_path[] = "D:/SERVER/storage";
char *root_path;


void createTextFileWithData(const char *filePath, const char *data,const int typ) {
    // Open the file in write mode, creating it if it doesn't exist
    FILE *file = fopen(filePath, "w");

	//type 0 string
	//type 1 number,bool
	//type 2 list

    if (file != NULL) {
        // Write data to the file
        if(typ == 0){
        	fputc('"',file);
        	fprintf(file, "%s", data);
		} else if(typ == 1){
			if(data[0] == 'T') {
				fputc('T',file);
			} else if(data[0] == 'F') {
				fputc('F',file);
			} else {
				fprintf(file, "%s", data);
			}
		} else if(typ == 2){
			fputc('[',file);
			fprintf(file, "%s", data);
			fputc(']',file);
		}
        fclose(file);
    } else {
        // File creation failed
        perror("Error creating file");
    }
}

// Function to traverse and print JSON data
void createFolder(const char *globePath) {
    // Combine the two path components
    char folderPath[1100] = "";
    
    sprintf(folderPath, "%s/%s",root_path, globePath);
    
//    printf("\nfolder %s\n",folderPath);
    // Check if the folder already exists
    struct stat st = {0};

    if (stat(folderPath, &st) == -1) {
        // Folder does not exist, create it
        
        if (mkdir(folderPath,0777) == 0) {
//        if (mkdir(folderPath) == 0) {
//            printf("Folder created: %s\n", folderPath);
        } else {
            perror("Error creating folder");
        }
    } else {
//        printf("Folder already exists: %s\n", folderPath);
    }

}

void traverseJSON(FILE *filePointer, int level) {
	char current_key_string[10000];
	char file_path[200] = "";
	char other_types_string[100] = "";
	char val = fgetc(filePointer);
	int ch = 0;
	
    int c = 0;
    int q = 0;
    int q2 = 0;
    int sqr = 0;
    
    int flag_for_numbers = 0;
    int ots = 0;
    
    while (val != EOF) {
    	
		if(q==0 && val == ']') {
			sqr--;
		}
		
		if(sqr == 0){
			switch(val){
	    		case '{':
	    			if(q == 1){
						current_key_string[ch] = val;
	    				ch++;
	    				break;
					}
	    			globe_img_path_ind[globe_img_ind] = globe_ind;
	    			globe_img_ind++;
	    			int g = 0;
	    			for(g=0;current_key_string[g] != '\0';g++){
	    				globe_path[globe_ind] = current_key_string[g];
	    				globe_ind++;
					}
					createFolder(globe_path);
	    			globe_path[globe_ind] = '\0';
	    			traverseJSON(filePointer,level+1);
	    			break;
	    		case '}':
	    			if(q == 1){
						current_key_string[ch] = val;
	    				ch++;
	    				break;
					}
					flag_for_numbers = 0;
    				if(ots > 1){
    					other_types_string[ots] = '\0';
//    					printf("\n----%s -> '%s'\n",file_path,&other_types_string[1]);//number,bool printing
	    				createTextFileWithData(file_path,&other_types_string[1],1);	
					}
	    			globe_img_ind--;
	    			globe_ind = globe_img_path_ind[globe_img_ind];
	    			globe_path[globe_ind] = '\0';
	    			return;
	    		case ':':
	    			if(q == 0){
	    				flag_for_numbers = 1;
	    				ots = 0;
	    				ch = 0;
	    				c=1;
					} else {
						current_key_string[ch] = val;
	    				ch++;
					}
					break;
				case '"':
					if(q == 0){
						q = 1;
						q2 = 1;
					} else {
						if(q2 == 1){
							q = 0;
							q2 = 0;						
						} else {
							current_key_string[ch] = val;
	    					ch++;
							break;
						}
					}
					break;
	    		case ',':
	    			if(q == 0){
	    				c=0;
	    				flag_for_numbers = 0;
	    				if(ots > 1){
	    					other_types_string[ots] = '\0';
//	    					printf("\n----%s -> '%s'\n",file_path,&other_types_string[1]);//number,bool printing
	    					createTextFileWithData(file_path,&other_types_string[1],1);	
	    					
						}
					} else {
						current_key_string[ch] = val;
	    				ch++;
					}
					break;
	    		case '\'':
					if(q == 0){
//						flag_for_numbers = 0;
	    				q = 1;
	    				ch = 0;
					} else {
						if(q2 == 1){
							current_key_string[ch] = val;
	    					ch++;
							break;
						}
						q = 0;
						current_key_string[ch] = '\0';
						if(c == 0){
							sprintf(file_path, "%s/%s/%s.txt",root_path, globe_path,current_key_string);
						} else {
//							printf("^%s^",current_key_string);//string printing
							createTextFileWithData(file_path,current_key_string,0);
						}
						
					}
					break;		
				case '[':
					if(q == 1){
						current_key_string[ch] = val;
	    				ch++;
	    				break;
					}
//					flag_for_numbers = 0;
					sqr = 1;
					ch = 0;
					
					break;
				case ']':
					if(q == 1){
						current_key_string[ch] = val;
	    				ch++;
	    				break;
					}
					current_key_string[ch] = '\0';
//					printf("^%s^",current_key_string);//list printing
					createTextFileWithData(file_path,current_key_string,2);
					sqr = 0;
					break;
	    		default:
    				if(q==1){
    					current_key_string[ch] = val;
    					ch++;
					} else {
						if(flag_for_numbers == 1){
							other_types_string[ots] = val;
							ots+=1;
						}
//							current_key_string[ch] = val;
//							ch++;
//						}
					}
			}
		} else {
			current_key_string[ch] = val;
	    	ch++;
		}
		val=fgetc(filePointer);
    }
}

int main(int argc, char *argv[]) {
	root_path = argv[1];
	int c = 0;
	
	if(argc<3){
		printf("Unable to proccess args.\n");
		return 1;
	}
	
	FILE *filePointer;
	filePointer = fopen(argv[2], "r");
	
	if (filePointer == NULL) {
        printf("Unable to open the file.\n");
        return 1; // Return an error code
    }
	
	fgetc(filePointer);
	traverseJSON(filePointer,0);
    fclose(filePointer);
    return 0;
}

