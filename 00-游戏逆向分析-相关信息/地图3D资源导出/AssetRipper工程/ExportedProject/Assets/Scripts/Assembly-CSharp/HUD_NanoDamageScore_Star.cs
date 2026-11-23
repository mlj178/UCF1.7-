using UnityEngine;
using UnityEngine.UI;

public class HUD_NanoDamageScore_Star : RecyclableObject
{
	[SerializeField]
	private RectTransform rectTransform;

	[SerializeField]
	private RawImage rawimage;

	private int index;

	private bool is500;

	private bool hide;

	private Vector2 targetPos1;

	private Vector2 targetPos2;

	private void OnDisable()
	{
	}

	protected override void OnEnable()
	{
	}

	public void SetData(int index, bool is500, bool hide)
	{
	}

	protected override void Work()
	{
	}

	public override void Recycle(bool roundRecycle)
	{
	}
}
