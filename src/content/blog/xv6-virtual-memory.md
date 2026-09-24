---
title: 'xv6의 가상 메모리를 직접 건드려봤다'
description: 'PTE bit 하나 바꿨을 뿐인데 TLB까지 따라왔다?'
pubDate: 'Sep 24 2026 15:00'
---

오늘 COMPSCI 340 Assignment 2를 마무리했다.

이번 과제에서 한 일을 한 줄로 요약하면:

> **페이지 테이블을 직접 돌아다니고, 권한을 바꾸고, 잘못된 메모리 접근까지 처리했다.**

수업에서 `Page Table`, `PTE`, `TLB`, `Page Fault`를 배울 때는 각각 별개의 개념처럼 느껴졌다.

그런데 xv6 안에서 직접 구현해보니 이 녀석들은 생각보다 훨씬 끈끈하게 엮여 있었다.

---

## System Call을 직접 추가해보기

먼저 새로운 system call을 xv6에 추가했다.

처음에는 system call 하나 추가하는 게 함수 하나 만드는 정도일 줄 알았는데, 당연히 그렇게 친절하지 않았다.

User program에서 system call을 호출하면 대략 다음과 같은 과정을 거친다.

```
User Program
    ↓
System Call Interface
    ↓
System Call Number
    ↓
Kernel System Call Handler
    ↓
Actual Kernel Function
```

평소 Linux에서 `read()`, `write()`, `fork()` 같은 system call을 아무 생각 없이 사용했는데, xv6에서 직접 하나를 추가해보니 user space와 kernel space 사이의 연결이 조금 더 현실적으로 보이기 시작했다.

---

## Page Table을 순회해서 사용 중인 메모리 계산하기

첫 번째 기능은 현재 사용 중인 메모리를 계산하는 `getusedmem`이었다.

기본적인 아이디어는 간단하다.

```
Used Memory = Valid Pages × 4096 bytes
```

하지만 xv6의 RISC-V 가상 메모리는 Sv39의 3단계 페이지 테이블을 사용한다.

따라서 배열 하나를 훑는 것으로 끝나는 것이 아니라 각 PTE를 확인하면서 invalid entry인지, 다음 level의 page table을 가리키는지, 실제 mapped page를 가리키는지를 구분해야 했다.

결국 page table을 재귀적으로 순회하면서 valid한 페이지를 계산하도록 구현했다.

이걸 직접 구현하고 나니 왜 페이지 테이블을 설명할 때 계속 tree 그림이 나오는지 이해됐다.

그냥 교수님들이 트리를 좋아해서 그리는 게 아니었다.

---

## `mprotect`로 메모리를 Read-Only로 만들기

다음으로 `mprotect`와 `munprotect`를 구현했다.

특정 virtual address에 해당하는 페이지를 찾아 PTE의 write permission을 직접 변경하는 방식이다.

핵심은 `PTE_W`였다.

`mprotect`에서는 이 bit를 제거하고, `munprotect`에서는 다시 추가한다.

재미있는 점은 포인터 자체에는 아무 변화가 없다는 것이다.

```
같은 pointer
같은 virtual address
같은 physical page

하지만 PTE_W 하나가 달라짐
        ↓
프로그램의 행동이 완전히 달라짐
```

bit 하나가 생각보다 권력이 세다.

그리고 PTE를 수정한 뒤에는 TLB에 남아 있는 이전 정보를 무효화하기 위해 `sfence_vma()`도 필요했다.

수업에서는 TLB를 단순히 주소 변환을 빠르게 해주는 캐시라고 생각했는데, 직접 kernel 코드를 수정해보니 캐시의 존재 자체가 코드의 correctness에도 영향을 줄 수 있다는 걸 알게 됐다.

---

## NULL Pointer를 진짜로 막아보기

또 하나 구현한 것은 NULL pointer 접근에 대한 보호였다.

예를 들어:

```c
int *p = 0;
*p = 10;
```

C를 배우면서 수도 없이 봤던 NULL pointer dereference다.

이번에는 xv6의 memory layout을 직접 수정하면서 왜 이런 접근이 실패하는지를 더 낮은 수준에서 확인할 수 있었다.

잘못된 virtual address에 접근하면 page table의 mapping과 permission을 만족하지 못하고 CPU exception이 발생한다. 이것이 trap을 통해 kernel로 전달되고, 결국 문제가 있는 process가 처리된다.

평소에는 그냥 `Segmentation fault` 한 줄로 끝났던 일이 실제로는 여러 계층을 거치고 있었다.

적어도 이제 죽었을 때 왜 죽었는지는 조금 더 잘 알게 됐다.

---

## 가장 오래 걸린 건 구현보다 `usertests`였다

코드를 구현하는 과정에서도 여러 번 막혔지만, 의외로 가장 오래 붙잡고 있었던 건 **A2 전체 `usertests` 실행**이었다.

전체 테스트를 실행했는데 터미널에 새로운 출력이 나오지 않았다.

1분, 2분...

계속 기다렸는데 아무것도 나오지 않았다.

결국 약 **8분 동안 출력이 없어서 테스트가 멈춘 것처럼 보였다.**

운영체제 과제에서 터미널이 8분 동안 조용하면 여러 생각이 든다.

```
무한 루프인가?
deadlock인가?
내 page table 코드가 뭔가 박살냈나?
그냥 느린 건가?
```

문제는 xv6 내부에서 긴 테스트가 실행되고 있으면 단순히 출력만 없는 것인지, 실제로 시스템이 멈춘 것인지 겉으로는 구분하기 어렵다는 점이었다.

그래서 처음에는 내가 구현한 memory 관련 코드에 문제가 있다고 의심했다.

그런데 기다린 뒤 테스트가 `diskfull` 단계까지 진행됐고, 이번에는 **테스트 스크립트 자체에서 `NameError`가 발생했다.**

즉 상황이 조금 더 복잡해졌다.

```
테스트가 오래 걸림
        ↓
멈춘 것처럼 보임
        ↓
내 구현 문제인가 의심
        ↓
diskfull까지 진행
        ↓
테스트 스크립트 NameError
```

결과적으로 전체 테스트의 최종 결과만 보고 내 구현이 잘못됐다고 판단하기 어려운 상황이었다.

이 과정에서 꽤 중요한 걸 배웠다.

> **테스트가 실패했다고 항상 내가 작성한 코드가 실패한 것은 아니다.**

내 코드, xv6 자체의 동작, 테스트 케이스, 그리고 테스트를 실행하는 스크립트까지 서로 분리해서 확인해야 했다.

특히 테스트가 오래 걸릴 때는 단순히 "멈췄다"고 판단하기보다 **어디까지 실행됐는지, CPU가 실제로 작업하고 있는지, 특정 테스트에서 재현되는지**를 확인하는 게 중요했다.

디버깅 대상이 항상 내 코드라는 보장은 없었다.

---

## 이번 과제에서 가장 크게 배운 것

이번 과제 전에는 다음 개념들이 각각 별개의 시험 범위처럼 느껴졌다.

```
Virtual Memory
Page Table
PTE
TLB
Page Fault
Trap
System Call
```

직접 xv6를 수정하고 테스트해보니 실제로는 하나의 흐름이었다.

```
User Program
      ↓
Virtual Address
      ↓
Page Table / PTE
      ↓
TLB
      ↓
Memory Access
      ↓
Page Fault
      ↓
Trap
      ↓
Kernel
```

그리고 기술적인 내용 외에도 하나 더 배웠다.

**구현하는 것과 구현이 제대로 동작한다는 것을 검증하는 것은 완전히 다른 문제다.**

코드를 다 작성했다고 과제가 끝나는 게 아니었다.

테스트가 오래 걸리면 정말 멈춘 것인지 확인해야 하고, 실패하면 내 코드의 문제인지 테스트 환경의 문제인지도 구분해야 했다.

어쩌면 이번 과제에서 가장 운영체제다운 경험은 page table을 수정한 순간보다 **8분 동안 아무 말 없는 터미널을 바라보면서 "이게 정상인가?" 고민했던 순간**이었는지도 모르겠다.

하지만 결국 과제를 끝냈고, 다음부터 터미널이 한동안 조용하더라도 바로 `Ctrl+C`부터 누르지는 않겠다는 작은 교훈도 얻었다.

**대답 없는 그대를 기다리며...**

