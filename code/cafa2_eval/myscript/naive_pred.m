function [] = naive_pred(matlab_path, cat, ont_db_path, oa_file, oa_train_file, benchmark_file, output_folder)
  addpath(matlab_path)
  ont = pfp_ontbuild(ont_db_path)
  if cat == 'BPO' | cat == 'bpo'
    ont = ont{1,1};
  elseif cat == 'CCO' | cat == 'cco'
    ont = ont{1,2};
  elseif cat == 'MFO' | cat == 'mfo'
    ont = ont{1,3};
  end
  oa = pfp_oabuild(ont, oa_file);
  benchmark = pfp_loaditem(benchmark_file, 'char');

  oa_train = pfp_oabuild(ont, oa_train_file);
  qseqid = benchmark;
  naive = pfp_naive(qseqid, oa_train);

  fmax = pfp_seqmetric(benchmark, naive, oa, 'fmax');
  pr = pfp_seqmetric(benchmark, naive, oa, 'pr');
  fmax
  if ~exist(output_folder, 'dir')
    mkdir(output_folder);
  end
  writetable(struct2table(fmax), strcat(output_folder,'/fmax.txt'));
  writetable(array2table(pr,'VariableNames',{'precision','recall'}), strcat(output_folder,'/prcurve.csv'));
end
