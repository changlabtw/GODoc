function [] = fmax(matlab_path, cat, ont_path, oa_file, pred_file, benchmark_file, output)
  addpath(matlab_path)
  ont = load(strcat(ont_path, cat, '.mat'));
  if cat == 'BPO'
    ont = ont.BPO;
  elseif cat == 'CCO'
    ont = ont.CCO;
  elseif cat == 'MFO'
    ont = ont.MFO;
  end
  oa = pfp_oabuild(ont, oa_file);
  pred = cafa_import(pred_file, ont);
  benchmark = pfp_loaditem(benchmark_file, 'char');
  fmax = pfp_seqmetric(benchmark, pred, oa, 'fmax');
  fmax
  writetable(struct2table(fmax), output)
end
