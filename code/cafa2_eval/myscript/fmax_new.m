function [] = fmax(matlab_path, cat, ont_path, oa_file, pred_file, benchmark_file, output)
  addpath(matlab_path)
  ont = pfp_ontbuild(ont_path)
  if cat == 'BPO'
    ont = ont{1,1};
  elseif cat == 'CCO'
    ont = ont{1,2};
  elseif cat == 'MFO'
    ont = ont{1,3};
  end
  oa = pfp_oabuild(ont, oa_file);
  pred = cafa_import(pred_file, ont);
  benchmark = pfp_loaditem(benchmark_file, 'char');
  fmax = pfp_seqmetric(benchmark, pred, oa, 'fmax');
  fmax
  writetable(struct2table(fmax), output)
end
