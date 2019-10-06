function [] = cafa_sheet_seq_fmax(sfile, fmax, fmax_bst, reg, isdump, anonymous)
%CAFA_SHEET_SEQ_FMAX CAFA sheet sequence-centric Fmax
%
% [] = CAFA_SHEET_SEQ_FMAX(sfile, fmax, fmax_bst, reg, isdump, anonymous);
%
%   Builds evaluation reports (*.csv).
%
% Input
% -----
% [char]
% sfile:    The filename of the report sheet.
%
% [cell]
% fmax:     1-by-n fmax results.
%           [char]      [1-by-k]    .id
%           [double]    [1-by-1]    .fmax
%           [double]    [1-by-1]    .point
%           [double]    [1-by-1]    .tau
%           [double]    [1-by-1]    .coverage
%           See cafa_eval_seq_fmax.m
%
% [cell]
% fmax_bst: 1-by-n bootstrapped fmax results.
%           [char]      [1-by-k]    .id
%           [double]    [B-by-1]    .fmax_bst
%           [double]    [B-by-1]    .point_bst
%           [double]    [B-by-1]    .tau_bst
%           [double]    [B-by-1]    .coverage_bst
%           See cafa_eval_seq_fmax_bst.m
%
% [char]
% reg:      The team register, which has the following columns:
%         * 1. <internalID>
%         * 2. <externalID>
%           3. <teamname>
%         * 4. <type>
%         * 5. <displayname>
%         * 6. <dumpname>
%           7. <pi>
%           8. <keyword list>
%           9. <assigned color>
%
%           Note:
%           1. The starred columns (*) will be used in this function.
%           2. 'type':  'q'  - qualified
%                       'd'  - disqualified
%                       'n'  - Naive method (baseline 1)
%                       'b'  - BLAST method (baseline 2)
%
% [logical]
% isdump:   A switch for using dump name instead of display name.
%           default: false
%
% [logical]
% anonymous:  Toggle for anonymous. (i.e. remove the team name column)
%
% Output
% ------
% None.
%
% Dependency
% ----------
%[>]cafa_team_register.m
%
% See Also
% --------
%[>]cafa_eval_seq_fmax.m
%[>]cafa_eval_seq_fmax_bst.m

  % check inputs {{{
  if nargin ~= 6
    error('cafa_sheet_seq_fmax:InputCount', 'Expected 6 inputs.');
  end

  % sfile
  validateattributes(sfile, {'char'}, {'nonempty'}, '', 'sfile', 1);
  fout = fopen(sfile, 'w');
  if fout == -1
    error('cafa_sheet_seq_fmax:FileErr', 'Cannot open file.');
  end

  % fmax
  validateattributes(fmax, {'cell'}, {'nonempty'}, '', 'fmax', 2);

  % fmax_bst
  validateattributes(fmax_bst, {'cell'}, {'nonempty'}, '', 'fmax_bst', 3);

  % reg
  validateattributes(reg, {'char'}, {'nonempty'}, '', 'reg', 4);
  [team_id, ext_id, ~, team_type, disp_name, dump_name] = cafa_team_register(reg);

  % isdump
  validateattributes(isdump, {'logical'}, {'nonempty'}, '', 'isdump', 5);
  if isdump
    disp_name = dump_name;
  end

  % anonymous
  validateattributes(anonymous, {'logical'}, {'nonempty'}, '', 'anonymous', 6);
  % }}}

  % prepare output {{{
  n = numel(fmax);
  for i = 1 : n
    if ~strcmp(fmax{i}.id, fmax_bst{i}.id)
      error('cafa_sheet_seq_fmax:IDErr', 'Bootstrapped ID mismatch.');
    end

    [found, index] = ismember(fmax{i}.id, team_id);
    if ~found
      error('cafa_sheet_seq_fmax:IDErr', 'Invalid model ID.');
    end
    fmax{i}.eid  = ext_id{index};
    fmax{i}.team = disp_name{index};
  end
  % }}}

  % printing {{{
  if anonymous
    header = strcat('ID-model', ',Coverage,F1-max,Threshold', ',Coverage Avg(B),F1-max Avg(B),F1-max Std(B),Threshold Avg(B)', '\n');
    format = '%s,%.2f,%.3f,%.2f,%.2f,%.3f,%.3f,%.2f\n';
    fprintf(fout, header);
    for i = 1 : n
      fprintf(fout, format, ...
        fmax{i}.eid, ...
        fmax{i}.coverage, ...
        fmax{i}.fmax, ...
        fmax{i}.tau, ...
        nanmean(fmax_bst{i}.coverage_bst), ...
        nanmean(fmax_bst{i}.fmax_bst), ...
        nanstd(fmax_bst{i}.fmax_bst), ...
        nanmean(fmax_bst{i}.tau_bst) ...
        );
    end
  else
    header = strcat('ID-model,Team', ',Coverage,F1-max,Threshold', ',Coverage Avg(B),F1-max Avg(B),F1-max Std(B),Threshold Avg(B)', '\n');
    format = '%s,%s,%.2f,%.3f,%.2f,%.2f,%.3f,%.3f,%.2f\n';
    fprintf(fout, header);
    for i = 1 : n
      fprintf(fout, format, ...
        fmax{i}.eid, ...
        fmax{i}.team, ...
        fmax{i}.coverage, ...
        fmax{i}.fmax, ...
        fmax{i}.tau, ...
        nanmean(fmax_bst{i}.coverage_bst), ...
        nanmean(fmax_bst{i}.fmax_bst), ...
        nanstd(fmax_bst{i}.fmax_bst), ...
        nanmean(fmax_bst{i}.tau_bst) ...
        );
    end
  end
  fclose(fout);
  % }}}
return
% }}}

% -------------
% Yuxiang Jiang (yuxjiang@indiana.edu)
% Department of Computer Science
% Indiana University Bloomington
% Last modified: Mon 23 May 2016 03:49:40 PM E
