import math

# Stack
def peek(stack):
    if stack:
        return stack[-1]
    else:
        return 0

def pop(stack):
    print("POP ", end = '')
    stack.pop()

def run(digit_pos, w):
    print(f"W={w} ", end ='')
    x = peek(z)

    match digit_pos:
        case 14:
            x += 13
        case 13:
            x += 11
        case 12:
            x += 15
        case 11:
            x += -6
            pop(z)
        case 10:
            x += 15
        case 9:
            x += -8
            pop(z)
        case 8:
            x += -4
            pop(z)
        case 7:
            x += 15
        case 6:
            x += 10
        case 5:
            x += 11
        case 4:
            x += -11
            pop(z)
        case 3:
            x += 0
            pop(z)
        case 2:
            x += -8
            pop(z)
        case 1:
            x += -7
            pop(z)

    if x != w:
        print("PUSH ", end='')
        y = w
        match digit_pos:
            case 14:
                y += 3
            case 13:
                y += 12
            case 12:
                y += 9
            case 11:
                y += 12
            case 10:
                y += 2
            case 9:
                y += 1
            case 8:
                y += 1
            case 7:
                y += 13
            case 6:
                y += 1
            case 5:
                y += 6
            case 4:
                y += 2
            case 3:
                y += 11
            case 2:
                y += 10
            case 1:
                y += 3
        z.append(y)
    print(f"x={x}, z={z}\n")

print("\n")
z = []
#code = [9, 1, 6, 9, 9, 3, 9, 4, 8, 9, 4, 9, 9, 5]

code = [5, 1, 1, 4, 7, 1, 9, 1, 1, 6, 1, 2, 6, 1]
for w in range(14, 0, -1):
    print(f"{w} ", end='')
    run(w, code[14 - w])

answer = ""
for x in code:
    answer += str(x)
print(answer)

