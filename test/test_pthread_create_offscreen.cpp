// Copyright 2016 The Emscripten Authors.  All rights reserved.
// Emscripten is available under two separate licenses, the MIT license and the
// University of Illinois/NCSA Open Source License.  Both these licenses can be
// found in the LICENSE file.

#include <assert.h>
#include <bits/errno.h>
#include <emscripten/emscripten.h>
#include <emscripten/html5.h>
#include <emscripten/threading.h>
#include <math.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


pthread_t thread0, thread1; 

void* thread_with_canvas(void* arg) {
  printf("Thread with canvas spawned!\n");
  return nullptr;
}

void* thread_without_canvas(void* arg) {
  printf("Thread without canvas spawned!\n");
  return nullptr;
}

int main() {
  pthread_attr_t attr;
  pthread_attr_init(&attr);
  emscripten_pthread_attr_settransferredcanvases(&attr, "#canvas");
  pthread_create(&thread0, &attr, thread_with_canvas, 0);
  
  pthread_create(&thread1, nullptr, thread_without_canvas, 0);

  int status{};
  pthread_join(thread0, (void**)&status);
  pthread_join(thread1, (void**)&status);
  puts("Finished.");
  return 0;
}
