
% Use this function to create the settings for our genetic algorithm.
% The filenum indicates with number to use to identify the files 
% containing info for each generation.
% Each run of the genetic algorithm should use a different filenum
function settings = gaset(filenum, varargin)

% Set up the default values
settings = [];
settings.filenum = filenum;
settings.numParents     = 40; % orig. 10;
settings.numChildren    = 40; % orig. 5 * settings.numParents;
settings.numGenerations = 5;
settings.selection      = 'tournament';% orig. 'truncation';
settings.crossover      = 'uniform';
settings.mutation       = 0.05; % std of normal distribution computed as mutation*value
settings.eliteCount     = 1; % orig. 0;
settings.tournamentSize = 2;

% varargin = "variable arguments in"
for i = 1 : 2 : length(varargin),
    settings = setfield(settings,varargin{i},varargin{i+1});
end;