% Create a solution for Exercises 5.2 and 5.3, page 88 using plan.pl

% State = state(Farmer, Wolf, Goat, Cabbage) with each in {left,right}.

% opposite sides
opp(left, right).
opp(right, left).

% safety check: not (wolf with goat alone) and not (goat with cabbage alone)
safe(state(F, W, G, C)) :-
    \+ (W = G, F \= W),    % wolf and goat together without farmer -> unsafe
    \+ (G = C, F \= G).    % goat and cabbage together without farmer -> unsafe

% moves:
% Farmer crosses alone
move(S, S2) :-
    S = state(F, W, G, C),
    opp(F, F2),
    S2 = state(F2, W, G, C),
    safe(S2).

% Farmer crosses with wolf (only possible if wolf is on same side as farmer)
move(S, S2) :-
    S = state(F, F, G, C),    % Wolf on same side as Farmer
    opp(F, F2),
    S2 = state(F2, F2, G, C),
    safe(S2).

% Farmer crosses with goat
move(S, S2) :-
    S = state(F, W, F, C),    % Goat on same side as Farmer
    opp(F, F2),
    S2 = state(F2, W, F2, C),
    safe(S2).

% Farmer crosses with cabbage
move(S, S2) :-
    S = state(F, W, G, F),    % Cabbage on same side as Farmer
    opp(F, F2),
    S2 = state(F2, W, G, F2),
    safe(S2).

% plan(State, Goal, PathSoFar, MovesList)
plan(State, State, _Path, [State]) :- !.
plan(State, Goal, Path, [State|Moves]) :-
    move(State, Next),
    \+ member(Next, Path),            % avoid revisiting states
    plan(Next, Goal, [Next|Path], Moves).

% write_move(+State1, +State2)
write_move(state(F1,W1,G1,C1), state(F2,W2,G2,C2)) :-
    F1 \= F2,
    From = F1, To = F2,
    findall(Name,
        ( member(Name-Pos1-Pos2,
                 [wolf-W1-W2, goat-G1-G2, cabbage-C1-C2]),
          Pos1 \= Pos2
        ),
        Movers),
    ( Movers == []
    -> format('Farmer crosses from ~w to ~w.~n', [From,To])
    ; atomic_list_concat(Movers, ' and ', Others),
      format('Farmer and ~w cross from ~w to ~w.~n', [Others,From,To])
    ).

% print_moves(+MovesList) - print each crossing step
print_moves([_]) :- !.
print_moves([S1,S2|Rest]) :-
    write_move(S1,S2),
    print_moves([S2|Rest]).

% convenience solve that uses the usual start/goal
solve :-
    Start = state(left,left,left,left),
    Goal  = state(right,right,right,right),
    plan(Start, Goal, [Start], Moves),
    print_moves(Moves).

% alternative: solve(Start,Goal) to use custom states
solve(Start, Goal) :-
    plan(Start, Goal, [Start], Moves),
    print_moves(Moves).

