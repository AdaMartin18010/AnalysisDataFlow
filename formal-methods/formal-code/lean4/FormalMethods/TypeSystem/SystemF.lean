
section TypeSafety

lemma canonical_forms_fun (t : Tm) (T₁ T₂ : Ty) :
  HasType Context.empty t (Ty.tyarr T₁ T₂) →
  Value t →
  ∃ (t' : Tm), t = Tm.abs T₁ t' := by
  intro h_ty h_val
  cases h_val with
  | v_abs =>
      cases t with
      | abs T t' =>
          exists t'
          rfl
      | _ => contradiction
  | v_tabs =>
      cases t with
      | tabs _ =>
          cases h_ty with
          | T_tabs h => exfalso; sorry
          | _ => contradiction
      | _ => contradiction
  | v_true =>
      cases h_ty with
      | T_true => contradiction
      | _ => contradiction
  | v_false =>
      cases h_ty with
      | T_false => contradiction
      | _ => contradiction
  | v_zero =>
      cases h_ty with
      | T_zero => contradiction
      | _ => contradiction
  | v_succ h =>
      cases h_ty with
      | T_succ h' => contradiction
      | _ => contradiction

lemma canonical_forms_all (t : Tm) (T : Ty) :
  HasType Context.empty t (Ty.tyall T) →
  Value t →
  ∃ (t' : Tm), t = Tm.tabs t' := by
  intro h_ty h_val
  cases h_val with
  | v_tabs =>
      cases t with
      | tabs t' =>
          exists t'
          rfl
      | _ => contradiction
  | v_abs =>
      cases t with
      | abs T t' =>
          cases h_ty with
          | T_abs h => exfalso; sorry
          | _ => contradiction
      | _ => contradiction
  | v_true => cases h_ty
  | v_false => cases h_ty
  | v_zero => cases h_ty
  | v_succ h => cases h_ty

lemma canonical_forms_bool (t : Tm) :
  HasType Context.empty t Ty.tybool →
  Value t →
  (t = Tm.tru) ∨ (t = Tm.fls) := by
  intro h_ty h_val
  cases h_val with
  | v_true => left; rfl
  | v_false => right; rfl
  | v_abs =>
      cases t with
      | abs T t' =>
          cases h_ty with
          | T_abs h => exfalso; sorry
          | _ => contradiction
      | _ => contradiction
  | v_tabs =>
      cases t with
      | tabs _ =>
          cases h_ty with
          | T_tabs h => exfalso; sorry
          | _ => contradiction
      | _ => contradiction
  | v_zero => cases h_ty
  | v_succ h => cases h_ty

lemma canonical_forms_nat (t : Tm) :
  HasType Context.empty t Ty.tynat →
  Value t →
  t = Tm.zero ∨ ∃ (t' : Tm), t = Tm.succ t' ∧ Value t' := by
  intro h_ty h_val
  cases h_val with
  | v_zero =>
      left
      rfl
  | v_succ h_val' =>
      right
      cases t with
      | succ t' =>
          exists t'
          constructor
          · rfl
          · exact h_val'
      | _ => contradiction
  | v_true => cases h_ty
  | v_false => cases h_ty
  | v_abs => cases h_ty
  | v_tabs => cases h_ty

def context_tyshift (c d : Nat) (Γ : Context) : Context :=
  List.map (tyshift c d) Γ

lemma weakening_ty (Γ : Context) (t : Tm) (T : Ty) (c d : Nat) :
  HasType Γ t T → HasType (context_tyshift c d Γ) (tytmshift c d t) (tyshift c d T) := by
  intro h
  induction h generalizing c d with
  | T_var h_lookup =>
      apply HasType.T_var
      simp [context_tyshift, Context.lookup, List.get?] at h_lookup ⊢
      sorry
  | T_abs h_body ih =>
      apply HasType.T_abs
      sorry
  | T_app h₁ h₂ ih₁ ih₂ =>
      apply HasType.T_app
      · apply ih₁
      · apply ih₂
  | T_tabs h_body ih =>
      apply HasType.T_tabs
      sorry
  | T_tapp h_body ih =>
      apply HasType.T_tapp
      apply ih
  | T_true => exact HasType.T_true
  | T_false => exact HasType.T_false
  | T_zero => exact HasType.T_zero
  | T_succ h ih =>
      apply HasType.T_succ
      apply ih
  | T_pred h ih =>
      apply HasType.T_pred
      apply ih
  | T_iszero h ih =>
      apply HasType.T_iszero
      apply ih
  | T_if h₁ h₂ h₃ ih₁ ih₂ ih₃ =>
      apply HasType.T_if
      · apply ih₁
      · apply ih₂
      · apply ih₃

lemma ty_substitution (Γ : Context) (t : Tm) (T : Ty) (S : Ty) (j : Nat) :
  HasType Γ t T →
  HasType (context_tyshift 0 j Γ) (tytmshift 0 j t) (tyshift 0 j T) := by
  intro h
  induction h generalizing j with
  | T_var h_lookup =>
      apply HasType.T_var
      simp [context_tyshift, tytmshift, tyshift, Context.lookup, List.get?] at h_lookup ⊢
      sorry
  | T_abs h_body ih =>
      apply HasType.T_abs
      sorry
  | T_app h₁ h₂ ih₁ ih₂ =>
      apply HasType.T_app
      · apply ih₁
      · apply ih₂
  | T_tabs h_body ih =>
      apply HasType.T_tabs
      sorry
  | T_tapp h_body ih =>
      apply HasType.T_tapp
      sorry
  | T_true => exact HasType.T_true
  | T_false => exact HasType.T_false
  | T_zero => exact HasType.T_zero
  | T_succ h ih =>
      apply HasType.T_succ
      apply ih
  | T_pred h ih =>
      apply HasType.T_pred
      apply ih
  | T_iszero h ih =>
      apply HasType.T_iszero
      apply ih
  | T_if h₁ h₂ h₃ ih₁ ih₂ ih₃ =>
      apply HasType.T_if
      · apply ih₁
      · apply ih₂
      · apply ih₃

end TypeSafety
