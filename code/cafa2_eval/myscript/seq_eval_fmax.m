function [] = seq_eval_fmax(matlab_path, cat, ont_db_path, oa_file, pred_file, benchmark_file, output_folder, evmode)
  addpath(matlab_path)
  if nargin < 8
    evmode = '1'
  else
    evmode = '2'
  end
  ont = pfp_ontbuild(ont_db_path)
  if cat == 'BPO' | cat == 'bpo'
    ont = ont{1,1};
  elseif cat == 'CCO' | cat == 'cco'
    ont = ont{1,2};
  elseif cat == 'MFO' | cat == 'mfo'
    ont = ont{1,3};
  end
  oa = pfp_oabuild(ont, oa_file);
  pred = cafa_import(pred_file, ont);
  benchmark = pfp_loaditem(benchmark_file, 'char');

  fmax = pfp_seqmetric(benchmark, pred, oa, 'fmax', 'evmode', evmode);
  fmax
  if ~exist(output_folder, 'dir')
    mkdir(output_folder);
  end
  if evmode == '1'
    writetable(struct2table(fmax), strcat(output_folder,'/fmax.txt'));
  else
    writetable(struct2table(fmax), strcat(output_folder,'/partial_fmax.txt'));
  end
end
