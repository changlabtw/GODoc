function [smin, point, t] = pfp_sminc(curve, tau, order)
%PFP_SMINC Semantic distance mininum (from) curve
%
% [smin, point, t] = PFP_SMINC(curve, tau);
%
%   Returns the minimum semantic (order 2) distance of a RU-MI curve.
%
% [smin, point, t] = PFP_SMINC(curve, tau, order);
%
%   Returns the minimum semantic distance of a RU-MI curve with a specific type
%   of norm.
%
% Note
% ----
% RU  - remaining uncertainty.
% MI  - misinformation.
%
% Input
% -----
% [double]
% curve:  A k-by-2 RU-MI matrix (i.e. a curve)
%
% [double]
% tau:    A 1-by-k increasing thresholds.
%
% (optional)
% [double]
% order:  Order of the norm
%         default: 2 (Euclidean)
%
% Output
% ------
% [double]
% smin:   The minimum semantic distance.
%
% [double]
% point:  The corresponding (RU, Mi) that produces 'smin'.
%
% [double]
% t:      The best corresponding threshold.

  % check inputs {{{
  if nargin < 2
    error('pfp_sminc:InputCount', 'Expected >= 2 inputs.');
  end

  if nargin == 2
    order = 2;
  end

  % curve
  validateattributes(curve, {'double'}, {'ncols', 2}, '', 'curve', 1);
  k = size(curve, 1);

  % tau
  validateattributes(tau, {'double'}, {'numel', k, 'increasing'}, '', 'tau', 2);

  % order
  validateattributes(order, {'double'}, {'real', 'positive'}, '', 'order', 3);
  % }}}

  % sanity check {{{
  if any(all(isnan(curve), 1))
    smin  = NaN;
    point = nan(1, 2);
    t     = NaN;
    return;
  end
  % }}}

  % calculation {{{
  RU = curve(:, 1);
  MI = curve(:, 2);

  % Note that f(x) = x^(1/order) is monotonic, so we don't need to compute it
  % for every point.
  sd_sq = RU .^ order + MI .^ order;
  smin_sq = min(sd_sq);

  % threshold is set to the highest possible one that yields this smin_sq
  index = max(find(sd_sq == smin_sq));
  smin  = sd_sq(index) .^ (1 / order);
  point = curve(index, :);
  t     = tau(index);
  % }}}
return

% -------------
% Yuxiang Jiang (yuxjiang@indiana.edu)
% Department of Computer Science
% Indiana University Bloomington
% Last modified: Mon 23 May 2016 06:11:47 PM E
