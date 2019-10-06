function [sel, bsl, info] = cafa_sel_top_seq_fmax(K, fmaxs, naive, blast, reg, isdump)
%CAFA_SEL_TOP_SEQ_FMAX CAFA select top sequence-centric Fmax
%
% [sel, bsl, info] = CAFA_SEL_TOP_SEQ_FMAX(fmaxs, naive, blast, reg, isdump);
%
%   Picks the top bootstrapped Fmax.
%
% Input
% -----
% [double]
% K:      The number of models to pick. If K is set to 0, this function will
%         be used to pick baseline models, i.e. the returning 'sel' will be {}.
%         If K is set to 'inf', this function returns all model (one per each
%         PI) in a sorted order.
%
% [cell]
% fmaxs:  The pre-calculated Fmax structures.
%         [char]      [1-by-n]    .id
%         [double]    [B-by-1]    .fmax_bst
%         [double]    [B-by-2]    .point_bst
%         [double]    [B-by-1]    .tau_bst
%         [double]    [B-by-1]    .ncovered_bst
%         [double]    [B-by-1]    .coverage_bst
%         See cafa_eval_seq_fmax_bst.m, cafa_collect.m
%
% [char]
% naive:  The method id of the naive baseline. E.g. BN4S
%         Could be empty: '' if not interested.
%
% [char]
% blast:  The method id of the blast baseline. E.g. BB4S
%         Could be empty: '' if not interested.
%
% [char]
% reg:    The team register, which should have the folloing columns:
%       * 1. <internalID>
%       * 2. <externalID>
%         3. <teamname>
%       * 4. <type>
%       * 5. <displayname>
%       * 6. <dumpname>
%       * 7. <pi>
%         8. <keyword list>
%       * 9. <assigned color>
%
%         Note:
%         1. The starred columns (*) will be used in this function.
%         2. 'type':  'q'  - qualified
%                     'd'  - disqualified
%                     'n'  - Naive model (baseline 1)
%                     'b'  - BLAST model (baseline 2)
%
% [logical]
% isdump: A switch for using dump name instead of display name.
%
% Output
% ------
% [cell]
% sel:  The bars and related information ready for plotting:
%       .fmax_mean  [double]  scalar, "bar height".
%       .fmax_q05   [double]  scalar, 5% quantiles.
%       .fmax_q95   [double]  scalar, 95% quantiles.
%       .coverage   [double]  scalar, averaged coverage.
%       .tag        [char]    tag of the model.
%       .pi_name    [char]    name of the PI.
%       .color      [double]  assigned color (1-by-3 RGB tuple).
%
% [cell]
% bsl:  The baseline bars and related information. Each cell has the
%       same structure as 'sel'.
%
% [struct]
% info: Extra information.
%       .all_mid  [cell]  Method name of all participating models.
%       .top_mid  [cell]  Method name of top K models (ranked from 1 to K)
%
% Dependency
% ----------
%[>]cafa_team_register.m
%
% See Also
% --------
%[>]cafa_collect.m
%[>]cafa_eval_seq_fmax_bst.m

  % check inputs {{{
  if nargin ~= 6
    error('cafa_sel_top_seq_fmax:InputCount', 'Expected 6 inputs.');
  end

  % K
  validateattributes(K, {'double'}, {'nonnegative'}, '', 'K', 1);

  % fmaxs
  validateattributes(fmaxs, {'cell'}, {'nonempty'}, '', 'fmaxs', 2);

  % naive
  validateattributes(naive, {'char'}, {}, '', 'naive', 3);

  % blast
  validateattributes(blast, {'char'}, {}, '', 'blast', 4);

  % reg
  validateattributes(reg, {'char'}, {}, '', 'reg', 5);
  [team_id, ext_id, ~, team_type, disp_name, dump_name, pi_name, ~, clr] = cafa_team_register(reg);

  % isdump
  validateattributes(isdump, {'logical'}, {'nonempty'}, '', 'isdump', 6);
  if isdump
    disp_name = dump_name;
  end
  % }}}

  % clean up and filter models {{{
  % 1. remove 'disqualified' models;
  % 2. set aside baseline models;
  % 3. match team names for display.
  % 4. calculate averaged Fmax.

  n = numel(fmaxs);
  qld = cell(1, n); % all qualified models
  bsl = cell(1, 2); % two baseline models
  avg_fmaxs = zeros(1, n);

  kept = 0;

  % parse model number 1, 2 or 3 from external ID {{{
  % model_num = cell(1, n);
  % for i = 1 : n
  %   splitted_id = strsplit(ext_id{i}, '-');
  %   model_num{i} = splitted_id{2};
  % end
  % }}}

  for i = 1 : n
    index = find(strcmp(team_id, fmaxs{i}.id));

    if strcmp(fmaxs{i}.id, naive)
      bsl{1}.fmax_mean = nanmean(fmaxs{i}.fmax_bst);
      bsl{1}.fmax_q05  = prctile(fmaxs{i}.fmax_bst, 5);
      bsl{1}.fmax_q95  = prctile(fmaxs{i}.fmax_bst, 95);
      bsl{1}.coverage  = nanmean(fmaxs{i}.coverage_bst);
      bsl{1}.tag       = sprintf('%s', disp_name{index});
      bsl{1}.pi_name   = pi_name{index};
      bsl{1}.color     = (hex2dec(reshape(clr{index}, 3, 2))/255)';
    elseif strcmp(fmaxs{i}.id, blast)
      bsl{2}.fmax_mean = nanmean(fmaxs{i}.fmax_bst);
      bsl{2}.fmax_q05  = prctile(fmaxs{i}.fmax_bst, 5);
      bsl{2}.fmax_q95  = prctile(fmaxs{i}.fmax_bst, 95);
      bsl{2}.coverage  = nanmean(fmaxs{i}.coverage_bst);
      bsl{2}.tag       = sprintf('%s', disp_name{index});
      bsl{2}.pi_name   = pi_name{index};
      bsl{2}.color     = (hex2dec(reshape(clr{index}, 3, 2))/255)';
    elseif strcmp(team_type(index), 'q') % qualified models
      % filtering {{{
      % skip models with 0 coverage
      if ~any(fmaxs{i}.coverage_bst)
        continue;
      end

      % skip models covering less than 10 proteins on average
      if mean(fmaxs{i}.ncovered_bst) < 10
        continue;
      end

      avg_fmax = nanmean(fmaxs{i}.fmax_bst);

      % skip models with 'NaN' Fmax values
      if isnan(avg_fmax)
        continue;
      end
      % }}}

      % collecting {{{
      kept = kept + 1;
      qld{kept}.mid       = fmaxs{i}.id; % for temporary useage, will be removed
      qld{kept}.fmax_mean = avg_fmax;
      qld{kept}.fmax_q05  = prctile(fmaxs{i}.fmax_bst, 5);
      qld{kept}.fmax_q95  = prctile(fmaxs{i}.fmax_bst, 95);
      qld{kept}.coverage  = nanmean(fmaxs{i}.coverage_bst);
      avg_fmaxs(kept)     = avg_fmax;
      qld{kept}.disp_name = disp_name{index};
      % qld{kept}.tag       = sprintf('%s-%s', disp_name{index}, model_num{index});
      qld{kept}.tag       = sprintf('%s', disp_name{index});
      qld{kept}.pi_name   = pi_name{index};
      qld{kept}.color     = (hex2dec(reshape(clr{index}, 3, 2))/255)';
      % }}}
    else
      % 'x' nop
    end
  end
  qld(kept+1 : end)       = []; % truncate the trailing empty cells
  avg_fmaxs(kept+1 : end) = [];
  % }}}

  % sort averaged Fmax and pick the top K {{{
  if K == 0
    sel = {};
  elseif isinf(K)
    % keep all models, sorted
    sel    = {};
    sel_pi = {};
    [~, index] = sort(avg_fmaxs, 'descend');
    for i = 1 : numel(qld)
      if ~ismember(qld{index(i)}.pi_name, sel_pi)
        % append a new model
        sel_pi = [sel_pi, qld{index(i)}.pi_name];
        sel    = [sel, qld{index(i)}];
      end
    end
  else
    % keep finding the next team until
    % 1. find K (= 10) models, or
    % 2. exhaust the list
    % Note that we only allow one model selected per PI.

    sel = cell(1, K);
    sel_pi = {};
    [~, index] = sort(avg_fmaxs, 'descend');
    nsel = 0;
    for i = 1 : numel(qld)
      if ~ismember(qld{index(i)}.pi_name, sel_pi)
        nsel = nsel + 1;
        sel_pi{end + 1} = qld{index(i)}.pi_name;
        sel{nsel} = qld{index(i)};
      end
      if nsel >= K
        break;
      end
    end
    if nsel < K
      warning('cafa_sel_top_seq_fmax:LessThanK', 'Only selected %d models.', nsel);
      sel(nsel + 1 : end) = [];
    end
  end
  % }}}

  % fill-up extra info {{{
  info.all_mid = cell(1, numel(qld));
  for i = 1 : numel(qld)
    info.all_mid{i} = qld{i}.mid;
  end

  info.top_mid = cell(1, numel(sel));
  for i = 1 : numel(sel)
    info.top_mid{i} = sel{i}.mid;
    sel{i} = rmfield(sel{i}, 'mid'); % remove temporary field: mid
  end
  % }}}
return

% -------------
% Yuxiang Jiang (yuxjiang@indiana.edu)
% Department of Computer Science
% Indiana University Bloomington
% Last modified: Mon 23 May 2016 04:45:28 PM E
