% Create a solution for Exercise 5.8(c)
:- dynamic fib_memo/2.

% Khởi tạo các giá trị cơ bản
fib_memo(0, 1).
fib_memo(1, 1).

% Giao diện: fib(N,R) dùng bảng fib_memo để trả lời hoặc tính rồi lưu lại
fib(N, R) :-
    integer(N), N >= 0,
    (   % nếu đã có trong bảng nhớ thì trả về ngay
        fib_memo(N, R)
    ->  true
    ;   % chưa có: tính đệ qui và lưu lại bằng asserta
        N > 1,
        N1 is N - 1, N2 is N - 2,
        fib(N1, R1),
        fib(N2, R2),
        R is R1 + R2,
        asserta(fib_memo(N, R))
    ).
