public class TransparentBuff : Buff
{
	public float cvAlpha;

	public float pvAlpha;

	public TransparentBuff(string name, float duration, Entity owner)
		: base(null, 0f, null)
	{
	}

	private void ModelInfo_Getter_Alpha(ref float cv, ref float pv)
	{
	}

	protected override void OnLifeEnd()
	{
	}
}
