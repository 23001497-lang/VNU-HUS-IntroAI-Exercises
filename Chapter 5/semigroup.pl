% Create a solution for Exercise 5.1, page 88. More precisely, you will attempt to prove the equality of left- and right-neutral elements of semigroups with PROLOG and fail. Try to explain why?

% Giả định một phép toán * (mul/3) mô phỏng cấu trúc semigroup
% Ví dụ: mul(X,Y,Z) nghĩa là X * Y = Z.

% Ta không đưa ra luật cụ thể nào cho mul/3 vì muốn mô tả tổng quát.
% Tuy nhiên, ta có thể định nghĩa "trái trung hòa" và "phải trung hòa":

left_neutral(E) :-
    \+ ( mul(E, X, R), R \= X ).

right_neutral(E) :-
    \+ ( mul(X, E, R), R \= X ).

% Thử chứng minh eL = eR (ý tưởng)
prove_neutral_equality :-
    left_neutral(EL),
    right_neutral(ER),
    ( EL = ER ->
        writeln('Prolog: EL = ER thành công.')
    ;
        writeln('Prolog: Không chứng minh được EL = ER.')
    ).


% Ghi kết quả ra file .lop

run_exercise :-
    tell('result.lop'),
    writeln('=== Exercise 5.1: Neutral elements in semigroups ==='),
    writeln(''),
    writeln('Mục tiêu: chứng minh EL = ER từ các định nghĩa trung hòa trái/phải.'),
    writeln(''),
    ( prove_neutral_equality ->
        writeln('Kết quả: Prolog đã chứng minh được EL = ER (nếu có facts cụ thể).')
    ;
        writeln('Kết quả: Prolog không thể chứng minh EL = ER.'),
        writeln('Lý do: Prolog không hỗ trợ định lượng ∀ và suy luận đẳng thức đại số.')
    ),
    writeln(''),
    writeln('Nguyên nhân kỹ thuật:'),
    writeln('- Prolog không thể biểu diễn mệnh đề "với mọi X" (universal quantifier).'),
    writeln('- Prolog sử dụng nhất quán cú pháp (=), không có suy luận đại số.'),
    writeln('- Định lý này cần hệ thống chứng minh đẳng thức (như E Prover, Prover9).'),
    told.


% Chạy tự động khi load file

:- initialization(run_exercise).
