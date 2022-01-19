#ifdef _WIN32
#include <windows.h>            
#endif

#include <string>
#include <fstream>
#include <vector>
#include <iostream>
#include <GL/glut.h>
#include <stdio.h>
#include <math.h>
#include <windows.h>
#include <stdlib.h>
#include <time.h>



using namespace std;


class Vertex {
public:
	float x, y, z;
	Vertex(float xn, float yn, float zn) {
		x = xn; y = yn; z = zn;
	}
};

class Source {
public:
	float x, y, z;
	int speed;
	float colorR, colorG, colorB;
	double size;
};


class Particle {
public:
	float x, y, z;
	float r, g, b;
	float v;
	int t;
	float dirX, dirY, dirZ;
	float osX, osY, osZ;
	double angle; double size;
};

vector<Particle> particles;
vector<Particle> particles_second;
Source src;



GLuint window;
GLuint sub_width = 512, sub_height = 512;

void myDisplay();
void myIdle();
void myReshape(int width, int height);
void myKeyboard(unsigned char theKey, int mouseX, int mouseY);

//void drawSource();
void drawParticles();
void drawParticlesSecond();
void drawParticle(Particle c);
GLuint LoadTextureRAW(const char* filename, int wrap);

//double maxH = 60.0;
double pi = 3.1415;

Source s2;
vector<Particle>;
GLuint tex;
Vertex ociste(0.0, 0.0, 50.0);

int main(int argc, char** argv)
{
	src.x = 0.0; src.y = 0; src.z = 0.0;
	s2.x = 350; s2.y = 350.0; s2.z = 0;
	src.speed = 7.5;
	s2.speed = 7.5;
	src.colorB = 0.5; src.colorG = 0.5; src.colorR = 0.0;
	s2.colorR = 0.0; s2.colorG = 1.0; s2.colorB = 0.0;
	src.size = 0.5;
	s2.size = 0.7;
	srand(time(NULL));

	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
	glutInitWindowSize(sub_width, sub_height);
	glutInitWindowPosition(300, 300);
	glutInit(&argc, argv);

	window = glutCreateWindow("2. labos");
	glutReshapeFunc(myReshape);
	glutDisplayFunc(myDisplay);
	glutKeyboardFunc(myKeyboard);
	glutIdleFunc(myIdle);
	tex = LoadTextureRAW("cestica.bmp", 1);

	glBlendFunc(GL_SRC_ALPHA, GL_ONE);					
	glEnable(GL_BLEND);


	glEnable(GL_TEXTURE_2D);
	glBindTexture(GL_TEXTURE_2D, tex);

	glutMainLoop();
	return 0;
}

void myReshape(int width, int height)
{
	sub_width = width;                      	
	sub_height = height;						

	glViewport(0, 0, sub_width, sub_height);	

	
	glMatrixMode(GL_PROJECTION);                
	glLoadIdentity();                           

	gluPerspective(45.0f, (GLfloat)width / (GLfloat)height, 0.1f, 150.0f);

	glMatrixMode(GL_MODELVIEW);                 
	glLoadIdentity();                           

	glLoadIdentity();							
	glClearColor(0.0f, 0.0f, 0.0f, 0.0f);		
	glClear(GL_COLOR_BUFFER_BIT);				
	glPointSize(1.0);							
	glColor3f(0.0f, 0.0f, 0.0f);				
}

int t = 0;

void myDisplay()
{

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glLoadIdentity();

	glTranslatef(ociste.x, ociste.y, -ociste.z);

	drawParticles();
	
	//drawParticlesSecond();

	glutSwapBuffers();
}

int currentTime = 0; int oldTime = 0;

void myIdle() {
	currentTime = glutGet(GLUT_ELAPSED_TIME);
	int timeInterval = currentTime - oldTime;
	if (timeInterval > 10) {

		// Raðanje èestica
		if (src.speed > 0) {
			int n = rand() % src.speed + 1;
			for (int j = 0; j < n; j++) {
				double x, y, z, norm;
				x = (rand() % 200 - 100) / (double)100;
				y = (rand() % 200 - 100) / (double)100;
				z = (rand() % 200 - 100) / (double)100;
				//cout << x << " " << y << " " << z << " ";
				norm = pow(pow(x, 2.0) + pow(y, 2.0) + pow(z, 2.0), 0.5);
				x /= norm; y /= norm; z /= norm;
				Particle particle;
				particle.x = src.x; particle.y = src.y; particle.z = src.z;
				particle.r = src.colorR; particle.g = src.colorG; particle.b = src.colorB;
				particle.v = 0.5;
				particle.dirX = x; particle.dirY = y; particle.dirZ = z;
				particle.t = 75 + (rand() % 21 - 10);
				//cout << particle.t << " " << endl;
				particle.size = src.size;
				particles.push_back(particle);
			}
		}
		
		if (s2.speed > 0) {
			int n = rand() % s2.speed + 1;
			for (int j = 0; j < n; j++) {
				double x, y, z, norm;
				x = (rand() % 200 - 100) / (double)100;
				y = (rand() % 200 - 100) / (double)100;
				z = (rand() % 200 - 100) / (double)100;
				//cout << x << " " << y << " " << z << " ";
				norm = pow(pow(x, 2.0) + pow(y, 2.0) + pow(z, 2.0), 0.5);
				x /= norm; y /= norm; z /= norm;
				Particle particle;
				particle.x = src.x; particle.y = src.y; particle.z = src.z;
				particle.r = src.colorR; particle.g = src.colorG; particle.b = src.colorB;
				particle.v = 0.5;
				particle.dirX = x; particle.dirY = y; particle.dirZ = z;
				particle.t = 75 + (rand() % 21 - 10);
				//cout << particle.t << " " << endl;
				particle.size = src.size;
				particles_second.push_back(particle);
			}

		}

		// Pomak
		for (int j = particles.size() - 1; j >= 0; j--) {
			
			particles.at(j).x += particles.at(j).v * particles.at(j).dirX; 
			particles.at(j).y += particles.at(j).v * particles.at(j).dirY;
			particles.at(j).z += particles.at(j).v * particles.at(j).dirZ;
			

			particles.at(j).t--;

			// mijenjanje boje s odumiranjem (plava prema crvenoj)
			if (particles.at(j).b > 0)
				particles.at(j).b -= 0.008;
			if (particles.at(j).r < 1.0)
				particles.at(j).r += 0.008;
			if (particles.at(j).t <= 0) 
				particles.erase(particles.begin() + j);
			
		}

		for (int j = particles_second.size() - 1; j >= 0; j--) {

			particles_second.at(j).x += particles_second.at(j).v * particles_second.at(j).dirX;
			particles_second.at(j).y += particles_second.at(j).v * particles_second.at(j).dirY;
			particles_second.at(j).z += particles_second.at(j).v * particles_second.at(j).dirZ;


			particles_second.at(j).t--;

			// mijenjanje boje s odumiranjem (plava prema crvenoj)
			if (particles_second.at(j).g > 0)
				particles_second.at(j).g -= 0.008;
			if (particles_second.at(j).b < 1.0)
				particles_second.at(j).b += 0.008;
			if (particles_second.at(j).t <= 0)
				particles_second.erase(particles_second.begin() + j);

		}


		myDisplay();
		oldTime = currentTime;
	}
}

void drawParticles() {
	for (int j = 0; j < particles.size(); j++) {
		drawParticle(particles.at(j));
	}
}

void drawParticlesSecond() {
	for (int j = 0; j < particles_second.size(); j++) {
		drawParticle(particles_second.at(j));
	}
}
void drawParticle(Particle p) {
	
	// translacija tamo gdje treba iscrtati
	glColor3f(p.r, p.g, p.b);
	glTranslatef(p.x, p.y, p.z);
	//glRotatef(c.kut, c.osX, c.osY, c.osZ);//
	glBegin(GL_QUADS);

	glTexCoord2d(0.0, 0.0);
	glVertex3f(-p.size, -p.size, 0.0);
	glTexCoord2d(1.0, 0.0);
	glVertex3f(-p.size, +p.size, 0.0);
	glTexCoord2d(1.0, 1.0);
	glVertex3f(+p.size, +p.size, 0.0);
	glTexCoord2d(0.0, 1.0);
	glVertex3f(+p.size, -p.size, 0.0);

	glEnd();
	//glRotatef(-p.angle, p.osX, p.osY, p.osZ);//
	// povratak u centar
	glTranslatef(-p.x, -p.y, -p.z);
}

int turnOff = -1;

void myKeyboard(unsigned char pressedKey, int mouseX, int mouseY) {
	if (pressedKey == 'a')
		src.x -= 0.5;
	if (pressedKey == 'd')
		src.x += 0.5;
	if (pressedKey == 'c')
		src.y -= 0.5;
	if (pressedKey == 'v')
		src.y += 0.5; 
	if (pressedKey == 'w')
		src.z -= 0.5;
	if (pressedKey == 's')
		src.z += 0.5;
	

	if (pressedKey == 'r') {
		if (turnOff == -1) {
			turnOff = src.speed;
			src.speed = 0;
		}
		else {
			src.speed = turnOff;
			turnOff = -1;
		}
	}

	if (pressedKey == 'y' && src.colorG > 0.0)
		src.colorG -= 0.02;
	if (pressedKey == 'x' && src.colorG < 1.0)
		src.colorG += 0.02;
	if (pressedKey == 't' && src.colorR > 0.0)
		src.colorR -= 0.02;
	if (pressedKey == 'z' && src.colorR < 1.0)
		src.colorR += 0.02;

	if (pressedKey == '+' && src.size < 3.0)
		src.size += 0.01;
	if (pressedKey == '-' && src.size > 0.05)
		src.size -= 0.01;
	
}


GLuint LoadTextureRAW(const char* filename, int wrap)
{
	GLuint texture;
	int width, height;
	BYTE* data;
	FILE* file;
	
	file = fopen(filename, "rb");
	if (file == NULL) {
		return 0;
	}

	width = 256;
	height = 256;
	data = (BYTE*)malloc(width * height * 3);

	fread(data, width * height * 3, 1, file);
	fclose(file);

	glGenTextures(1, &texture);

	glBindTexture(GL_TEXTURE_2D, texture);

	glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);

	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
		GL_LINEAR_MIPMAP_NEAREST);
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,
		wrap ? GL_REPEAT : GL_CLAMP);
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,
		wrap ? GL_REPEAT : GL_CLAMP);

	gluBuild2DMipmaps(GL_TEXTURE_2D, 3, width, height,
		GL_RGB, GL_UNSIGNED_BYTE, data);

	free(data);

	return texture;
}