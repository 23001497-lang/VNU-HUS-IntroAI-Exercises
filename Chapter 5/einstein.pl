% Create a solution for Exercise 5.9, page 89
% Einstein's riddle solved with CLP(FD)
% Compatible with SWI-Prolog (use: swipl -s einstein_clp.pl -g solve -t halt)
% Also should run with GNU Prolog if clpfd is available.

:- use_module(library(clpfd)).

solve :-
    % Variables: each value is the house index 1..5
    Vars = [Brit,Swede,Dane,German,Norwegian,
            Red,Green,White,Yellow,Blue,
            Tea,Coffee,Milk,Beer,Water,
            PallMall,Dunhill,Marlboro,Rothmanns,Winfield,
            Dog,Bird,Cat,Horse,Fish],
    Vars ins 1..5,

    % values inside each attribute-group must be all different
    all_different([Brit,Swede,Dane,German,Norwegian]),
    all_different([Red,Green,White,Yellow,Blue]),
    all_different([Tea,Coffee,Milk,Beer,Water]),
    all_different([PallMall,Dunhill,Marlboro,Rothmanns,Winfield]),
    all_different([Dog,Bird,Cat,Horse,Fish]),

    % Constraints from the puzzle (mapping value <-> house index)
    Brit #= Red,                     % Brit lives in the red house
    Swede #= Dog,                    % Swede has a dog
    Dane #= Tea,                     % Dane drinks tea
    Green + 1 #= White,              % green is immediately left of white
    Green #= Coffee,                 % owner of green drinks coffee
    PallMall #= Bird,                % Pall Mall smoker has a bird
    Milk #= 3,                       % middle house drinks milk
    Yellow #= Dunhill,               % yellow house owner smokes Dunhill
    Norwegian #= 1,                  % Norwegian in the first house
    abs(Marlboro - Cat) #= 1,        % Marlboro next to the one who has a cat
    abs(Horse - Dunhill) #= 1,       % horse next to Dunhill smoker
    Winfield #= Beer,                % Winfield smoker drinks beer
    abs(Norwegian - Blue) #= 1,      % Norwegian next to the blue house
    German #= Rothmanns,             % German smokes Rothmanns
    abs(Marlboro - Water) #= 1,      % Marlboro smoker next to water drinker

    % Label (search for solutions)
    labeling([ff], Vars),

    % After labeling, we can print a readable table
    writeln('House\tColor\tNationality\tDrink\tSmoke\tPet'),
    forall(between(1,5,H), (
        color_name(H, Red,Green,White,Yellow,Blue, Color),
        nat_name(H, Brit,Swede,Dane,German,Norwegian, Nation),
        drink_name(H, Tea,Coffee,Milk,Beer,Water, Drink),
        smoke_name(H, PallMall,Dunhill,Marlboro,Rothmanns,Winfield, Smoke),
        pet_name(H, Dog,Bird,Cat,Horse,Fish, Pet),
        format('~d\t~w\t~w\t~w\t~w\t~w~n',[H,Color,Nation,Drink,Smoke,Pet])
    )),

    % Find who owns the fish
    FishPos = Fish,
    nat_name(FishPos, Brit,Swede,Dane,German,Norwegian, FishOwner),
    format('\nThe fish belongs to: ~w (house ~d)~n', [FishOwner, FishPos]),
    !.

% Helper predicates to translate house index into atom names
color_name(H, Red,Green,White,Yellow,Blue, Color) :-
    (Red=H -> Color = red ; Green=H -> Color = green ; White=H -> Color = white ; Yellow=H -> Color = yellow ; Blue=H -> Color = blue).

nat_name(H, Brit,Swede,Dane,German,Norwegian, Nation) :-
    (Brit=H -> Nation = brit ; Swede=H -> Nation = swede ; Dane=H -> Nation = dane ; German=H -> Nation = german ; Norwegian=H -> Nation = norwegian).

drink_name(H, Tea,Coffee,Milk,Beer,Water, Drink) :-
    (Tea=H -> Drink = tea ; Coffee=H -> Drink = coffee ; Milk=H -> Drink = milk ; Beer=H -> Drink = beer ; Water=H -> Drink = water).

smoke_name(H, PallMall,Dunhill,Marlboro,Rothmanns,Winfield, Smoke) :-
    (PallMall=H -> Smoke = pall_mall ; Dunhill=H -> Smoke = dunhill ; Marlboro=H -> Smoke = marlboro ; Rothmanns=H -> Smoke = rothmanns ; Winfield=H -> Smoke = winfield).

pet_name(H, Dog,Bird,Cat,Horse,Fish, Pet) :-
    (Dog=H -> Pet = dog ; Bird=H -> Pet = bird ; Cat=H -> Pet = cat ; Horse=H -> Pet = horse ; Fish=H -> Pet = fish).

% small convenience predicate to start when loading the file interactively
:- initialization(solve, main).
