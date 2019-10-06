function [] = blast_pred(matlab_path, cat, ont_db_path, test_oa_file, train_oa_file, blast_pred_file, target_file, benchmark_file, output_folder)
  addpath(matlab_path)
  ont = pfp_ontbuild(ont_db_path)
  if cat == 'BPO' | cat == 'bpo'
    ont = ont{1,1};
  elseif cat == 'CCO' | cat == 'cco'
    ont = ont{1,2};
  elseif cat == 'MFO' | cat == 'mfo'
    ont = ont{1,3};
  end
  test_oa = pfp_oabuild(ont, test_oa_file);
  benchmark = pfp_loaditem(benchmark_file, 'char');

  qseqid = pfp_loaditem(target_file, 'char');
  train_oa = pfp_oabuild(ont, train_oa_file);
  B = pfp_importblastp(blast_pred_file);
  blast = pfp_blast(qseqid, B, train_oa);

  fmax = pfp_seqmetric(benchmark, blast, test_oa, 'fmax');
  pr = pfp_seqmetric(benchmark, blast, test_oa, 'pr');
  fmax
  if ~exist(output_folder, 'dir')
    mkdir(output_folder);
  end
  writetable(struct2table(fmax), strcat(output_folder,'/fmax.txt'));
  writetable(array2table(pr,'VariableNames',{'precision','recall'}), strcat(output_folder,'/prcurve.csv'));
end
