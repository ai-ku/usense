function runiso(fname)
s = RandStream('mcg16807','Seed', 0);
RandStream.setDefaultStream(s);

PATH = '/home/tyr/playground/usense/';
addpath([PATH, 'bin/']);


reduced = [2 4 8 16];
options = struct('dims', reduced, 'overlay', 0, 'comp', 1, 'display', 0, 'dijkstra', 1, 'verbose', 1)

%d = readsparse('<zcat /home/tyr/playground/usense/run/test.knn.gz', 100);
d = readsparse(['<cat ' fname], 1000);
[~, column] = size(d);
D = max(d, d');


out_fname = regexp(fname, '\/', 'split');
out_fname = out_fname(end);
out_fname = out_fname{1};
%out_fname = out_fname(1:end-7);

[Y, ~, ~] = IsomapII(D, 'k', column-1, options);

% For debug purpose
%save('yre.100nn.2048.mat', 'Y', 'R', 'E');

disp(fname);
for i = 1:length(reduced)
    A = Y.coords{i}';
    [~, n] = size(A);
    dlmwrite([PATH, 'run/iso/', out_fname, '.iso.c' int2str(n)], A, 'delimiter', ' ');
end
exit;
%A = fscanf(fopen('weigh.v.dist.0.iso.c2'), '%f %f\n', [2, inf])'
end
