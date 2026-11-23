using UnityEngine;
using UnityEngine.UI;

public class HUD_NanoDamageScore_Effect : RecyclableObject
{
	[SerializeField]
	private RectTransform rectTransform;

	[SerializeField]
	private RawImage image;

	private Vector3 targetPos;

	protected override void Work()
	{
	}

	public override void Recycle(bool roundRecycle)
	{
	}

	public void SetPos(Vector3 bornPos, Vector3 targetPos)
	{
	}
}
